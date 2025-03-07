# 文件说明：`tokio-stream/src/wrappers/mpsc_unbounded.rs`

## 目的
该文件提供了一个适配器结构体 `UnboundedReceiverStream`，用于将 Tokio 的无界通道接收端（`tokio::sync::mpsc::UnboundedReceiver`）包装为实现了 `Stream` trait 的类型。这使得无界通道可以直接用于基于流（Stream）的异步处理，例如通过 `StreamExt` 的扩展方法进行迭代。

---

## 关键组件

### 1. **结构体定义**
```rust
pub struct UnboundedReceiverStream<T> {
    inner: UnboundedReceiver<T>,
}
```
- **功能**：包装原始的 `UnboundedReceiver<T>`，使其具备 `Stream` 特性。
- **成员**：
  - `inner`: 存储实际的无界通道接收端。

---

### 2. **方法实现**

#### a. **构造方法**
```rust
pub fn new(recv: UnboundedReceiver<T>) -> Self {
    Self { inner: recv }
}
```
- **功能**：通过 `UnboundedReceiver` 创建 `UnboundedReceiverStream` 实例。

#### b. **获取内部接收器**
```rust
pub fn into_inner(self) -> UnboundedReceiver<T> {
    self.inner
}
```
- **功能**：将包装器转换回原始的 `UnboundedReceiver`。

#### c. **关闭通道**
```rust
pub fn close(&mut self) {
    self.inner.close();
}
```
- **功能**：关闭发送端，阻止新消息发送，但仍允许接收缓冲区中的消息。

---

### 3. **Stream Trait 实现**
```rust
impl<T> Stream for UnboundedReceiverStream<T> {
    type Item = T;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        self.inner.poll_recv(cx)
    }
}
```
- **核心逻辑**：通过调用 `UnboundedReceiver` 的 `poll_recv` 方法实现 `poll_next`，使流的行为与原始接收器一致。

---

### 4. **辅助 Trait 实现**
- **`AsRef` 和 `AsMut`**：
  ```rust
  impl<T> AsRef<UnboundedReceiver<T>> for UnboundedReceiverStream<T> { ... }
  impl<T> AsMut<UnboundedReceiver<T>> for UnboundedReceiverStream<T> { ... }
  ```
  - **功能**：允许通过包装器直接访问内部接收器。

- **`From` Trait**：
  ```rust
  impl<T> From<UnboundedReceiver<T>> for UnboundedReceiverStream<T> { ... }
  ```
  - **功能**：提供从 `UnboundedReceiver` 直接转换为 `UnboundedReceiverStream` 的语法糖。

---

## 使用示例
```rust
use tokio::sync::mpsc;
use tokio_stream::wrappers::UnboundedReceiverStream;

#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::unbounded_channel();
    tx.send(10).unwrap();
    tx.send(20).unwrap();

    let mut stream = UnboundedReceiverStream::new(rx);
    assert_eq!(stream.next().await, Some(10));
    assert_eq!(stream.next().await, Some(20));
    assert_eq!(stream.next().await, None);
}
```
- **流程**：
  1. 创建无界通道并发送消息。
  2. 将接收端包装为流。
  3. 通过 `next().await` 异步消费消息。

---

## 项目中的角色