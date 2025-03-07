# `framed_read.rs` 文件详解

## 文件目的
该文件定义了 `FramedRead` 结构体，用于将异步字节流（`AsyncRead`）通过解码器（`Decoder`）转换为结构化消息流（`Stream`）。它是 Tokio 框架中处理基于帧协议的异步读取的核心组件，实现了从原始字节到应用层消息的解码功能。

---

## 关键组件

### 1. **结构体定义**
```rust
pub struct FramedRead<T, D> {
    #[pin]
    inner: FramedImpl<T, D, ReadFrame>,
}
```
- **`inner`**: 内部状态由 `FramedImpl` 管理，包含：
  - 底层 I/O 流 (`T: AsyncRead`)
  - 解码器 (`D: Decoder`)
  - 状态 (`ReadFrame`)，包括缓冲区 (`BytesMut`)、EOF 标志等。

---

### 2. **核心功能方法**
#### 初始化方法
```rust
pub fn new(inner: T, decoder: D) -> FramedRead<T, D> { ... }
pub fn with_capacity(inner: T, decoder: D, capacity: usize) -> FramedRead<T, D> { ... }
```
- `new`: 创建默认缓冲区大小的 `FramedRead`。
- `with_capacity`: 允许指定初始缓冲区大小，避免频繁扩容。

#### 状态访问方法
```rust
pub fn get_ref(&self) -> &T { ... }
pub fn get_mut(&mut self) -> &mut T { ... }
pub fn into_inner(self) -> T { ... }
```
- 提供安全访问底层 I/O 流的方法，但需注意避免破坏数据流完整性。

#### 解码器操作
```rust
pub fn decoder(&self) -> &D { ... }
pub fn map_decoder<C, F>(self, map: F) -> FramedRead<T, C> { ... }
```
- `decoder`: 获取解码器引用。
- `map_decoder`: 转换解码器类型，保留缓冲区数据。

---

### 3. **Trait 实现**
#### `Stream` 实现
```rust
impl<T, D> Stream for FramedRead<T, D> where T: AsyncRead, D: Decoder {
    type Item = Result<D::Item, D::Error>;
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> { ... }
}
```
- 通过 `poll_next` 轮询解码数据：
  1. 从底层 I/O 流读取字节到缓冲区。
  2. 使用解码器解析缓冲区中的数据。
  3. 返回解码后的消息或错误。

#### `Sink` 实现
```rust
impl<T, I, D> Sink<I> for FramedRead<T, D> where T: Sink<I> { ... }
```
- 委托写操作给底层 I/O 流，支持同时处理读写场景（如双向流）。

#### 调试支持
```rust
impl<T, D> fmt::Debug for FramedRead<T, D> { ... }
```
- 打印底层 I/O 流、解码器状态、缓冲区内容等调试信息。

---

## 工作原理
1. **数据流处理**：
   - 从 `AsyncRead` 读取字节到内部缓冲区。
   - 使用 `Decoder` 解码缓冲区中的字节，生成应用层消息。
   - 将解码结果作为 `Stream` 的项输出。

2. **缓冲区管理**：
   - 自动管理缓冲区大小，避免数据碎片。
   - 在解码未完成时保留未处理的字节，等待后续数据。

3. **错误处理**：
   - 若解码失败，返回错误并停止流（除非解码器支持恢复）。
   - 支持 `Decoder` 自定义错误类型。

---

## 项目中的角色