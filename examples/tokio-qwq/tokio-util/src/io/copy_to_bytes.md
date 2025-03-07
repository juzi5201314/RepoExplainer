# 文件说明：`copy_to_bytes.rs`

## 文件目的
该文件实现了 `CopyToBytes` 结构体，用于将一个接受 `Bytes` 类型的 `Sink` 转换为可接受 `&[u8]` 切片的 `Sink`。通过将传入的字节切片复制到 `Bytes` 所有权类型，解决了异步流处理中借用类型与所有权类型不兼容的问题。

---

## 核心组件

### 1. `CopyToBytes<S>` 结构体
```rust
pin_project! {
    #[derive(Debug)]
    pub struct CopyToBytes<S> {
        #[pin]
        inner: S,
    }
}
```
- **功能**：包装原始 `Sink<Bytes>`，提供 `Sink<&[u8]>` 接口。
- **关键特性**：
  - 使用 `pin_project` 宏处理异步环境中的指针逻辑。
  - 通过 `#[pin]` 标记 `inner` 字段，确保正确跟踪内部 `Sink` 的生命周期。

---

### 2. 方法实现
#### 构造与访问方法
```rust
impl<S> CopyToBytes<S> {
    pub fn new(inner: S) -> Self { ... }
    pub fn get_ref(&self) -> &S { ... }
    pub fn get_mut(&mut self) -> &mut S { ... }
    pub fn into_inner(self) -> S { ... }
}
```
- 提供对内部 `Sink` 的创建、只读访问、可变访问和所有权回收功能。

---

### 3. `Sink<&'a [u8]>` 特性实现
```rust
impl<'a, S> Sink<&'a [u8]> for CopyToBytes<S>
where
    S: Sink<Bytes>,
{
    // 实现四个核心方法
}
```
- **关键逻辑**：
  - `start_send` 方法将 `&[u8]` 转换为 `Bytes`：`Bytes::copy_from_slice(item)`。
  - 其他方法（`poll_ready`、`poll_flush` 等）直接转发到内部 `Sink` 的对应方法。
- **作用**：通过内存拷贝实现类型适配，使 `CopyToBytes` 可以安全地将借用切片传递给需要所有权的 `Sink`。

---

### 4. `Stream` 特性实现
```rust
impl<S: Stream> Stream for CopyToBytes<S> {
    type Item = S::Item;
    fn poll_next(...) { ... }
}
```
- 当内部 `Sink` 同时实现 `Stream` 时，`CopyToBytes` 会继承其流行为，直接转发 `poll_next` 调用。

---

## 在项目中的角色
该文件为 Tokio 异步 I/O 工具库提供了类型适配功能，通过将 `&[u8]` 自动转换为 `Bytes`，弥合了需要借用切片的生产者与需要所有权的消费者之间的类型差异，是构建异步流处理管道的重要中间件。
