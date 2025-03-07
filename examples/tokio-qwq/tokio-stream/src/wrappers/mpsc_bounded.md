# 文件解释：`tokio-stream/src/wrappers/mpsc_bounded.rs`

## **目的**  
该文件定义了一个名为 `ReceiverStream` 的结构体，用于将 Tokio 的有界通道接收端（`tokio::sync::mpsc::Receiver`）适配为符合 `Stream` trait 的异步流。其核心目标是让开发者能够通过统一的流接口（如 `next()` 或 `for await`）来消费通道中的消息。

---

## **关键组件**

### **1. `ReceiverStream` 结构体**
- **定义**：  
  ```rust
  pub struct ReceiverStream<T> {
      inner: Receiver<T>,
  }
  ```
  - 包含一个 `Receiver<T>` 字段 `inner`，用于存储实际的通道接收端。

- **方法**：
  - **`new(recv: Receiver<T>) -> Self`**：  
    通过传入 `Receiver` 实例创建 `ReceiverStream`。
  - **`into_inner(self) -> Receiver<T>`**：  
    将 `ReceiverStream` 转换回原始的 `Receiver`。
  - **`close(&mut self)`**：  
    关闭通道的发送端，阻止新消息发送，但允许继续接收缓冲区中的消息。

### **2. 实现 `Stream` Trait**
- **`poll_next` 方法**：  
  ```rust
  fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
      self.inner.poll_recv(cx)
  }
  ```
  - 直接调用 `Receiver` 的 `poll_recv` 方法，使 `ReceiverStream` 的行为与通道接收端一致，符合 `Stream` 的轮询逻辑。

### **3. 其他 Trait 实现**
- **`AsRef<Receiver<T>>` 和 `AsMut<Receiver<T>>`**：  
  允许通过 `as_ref()` 和 `as_mut()` 直接访问内部的 `Receiver`。
- **`From<Receiver<T>>`**：  
  支持通过 `From` trait 直接从 `Receiver` 转换为 `ReceiverStream`。

---

## **如何适配 Tokio 的通道到流接口**
- **适配逻辑**：  
  `ReceiverStream` 通过实现 `Stream` trait，将 Tokio 的 `Receiver` 的 `poll_recv` 方法映射为流的 `poll_next`，使得通道可以无缝集成到基于流的异步编程模型中。
- **使用示例**：  
  ```rust
  let (tx, rx) = mpsc::channel(2);
  let mut stream = ReceiverStream::new(rx);
  assert_eq!(stream.next().await, Some(10)); // 使用 Stream 接口消费消息
  ```

---

## **在项目中的角色**