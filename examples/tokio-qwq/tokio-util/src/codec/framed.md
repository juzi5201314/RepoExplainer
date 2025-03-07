# `framed.rs` 文件详解

## 文件目的
该文件定义了 `Framed` 结构体，提供了一个统一的异步流（`Stream`）和异步 Sink（`Sink`）接口，用于在底层 I/O 对象（如 TCP 连接）上实现基于帧的编码和解码。通过 `Encoder` 和 `Decoder` 特性 trait，它将原始字节流转换为有意义的帧（frame），适用于需要处理协议帧的场景（如 HTTP、自定义二进制协议等）。

---

## 核心组件

### 1. **`Framed` 结构体**
```rust
pub struct Framed<T, U> {
    #[pin]
    inner: FramedImpl<T, U, RWFrames>
}
```
- **功能**：封装了底层 I/O 对象（如 `TcpStream`）和编解码器（`Encoder`/`Decoder`），提供流式读取和 Sink 写入接口。
- **关键字段**：
  - `inner`: 内部实现逻辑由 `FramedImpl` 处理，包含 I/O 对象、编解码器实例以及读写缓冲区（`BytesMut`）。

---

### 2. **核心方法**
#### 初始化方法
- **`new`**  
  创建 `Framed` 实例，使用默认缓冲区大小：
  ```rust
  pub fn new(inner: T, codec: U) -> Framed<T, U> { ... }
  ```
- **`with_capacity`**  
  指定初始读缓冲区大小：
  ```rust
  pub fn with_capacity(inner: T, codec: U, capacity: usize) -> Framed<T, U> { ... }
  ```

#### 缓冲区与状态管理
- **`read_buffer`/`write_buffer`**  
  提供对读写缓冲区的引用，用于直接操作缓冲数据。
- **`backpressure_boundary`**  
  控制写缓冲区的阈值，超过阈值时暂停写入以避免内存溢出。

#### 低级访问
- **`get_ref`/`get_mut`**  
  安全地访问底层 I/O 对象和编解码器，但需注意避免破坏帧流一致性。
- **`into_inner`/`into_parts`**  
  将 `Framed` 解构为原始 I/O 对象、编解码器和缓冲区，便于复用或自定义逻辑。

---

### 3. **实现的 trait**
#### `Stream` trait 实现
```rust
impl<T, U> Stream for Framed<T, U> where T: AsyncRead, U: Decoder { ... }
```
- **功能**：从底层 I/O 读取字节流，通过 `Decoder` 解码为帧（`Item`），并作为流元素返回。
- **关键方法**：`poll_next` 委托给内部 `FramedImpl` 的实现。

#### `Sink` trait 实现
```rust
impl<T, I, U> Sink<I> for Framed<T, U> where T: AsyncWrite, U: Encoder<I> { ... }
```
- **功能**：将应用层的帧（`Item`）通过 `Encoder` 编码为字节，并写入底层 I/O。
- **关键方法**：`start_send`、`poll_flush` 等方法委托给 `FramedImpl`。

---

### 4. **`FramedParts` 结构体**
```rust
pub struct FramedParts<T, U> {
    pub io: T,
    pub codec: U,
    pub read_buf: BytesMut,
    pub write_buf: BytesMut,
    _priv: (),
}
```
- **用途**：将 `Framed` 的内部状态（I/O、编解码器、缓冲区）导出为可复用的部件，支持创建新 `Framed` 实例或更换编解码器。

---

## 关键特性
1. **帧化处理**  
   将字节流拆分为逻辑帧（如 HTTP 消息、自定义协议包），通过 `Decoder` 和 `Encoder` 实现协议无关性。
   
2. **缓冲管理**  
   使用 `BytesMut` 管理读写缓冲区，支持动态调整缓冲区大小（`with_capacity`）和背压控制（`backpressure_boundary`）。

3. **取消安全性**  
   - `Sink::send` 在被取消时保证消息未发送但可能丢失。
   - `Stream::next` 的未来对象不会因丢弃而丢失数据。

4. **灵活性**  
   通过 `into_parts` 和 `from_parts` 支持自定义编解码器或缓冲区逻辑，适用于复杂协议栈（如 TLS、压缩层）。

---

## 在项目中的角色