### 文件解释：`tokio-util/src/io/reader_stream.rs`

#### **目的**
该文件实现了 `ReaderStream` 结构体，用于将 Tokio 的 `AsyncRead` 对象（如文件、网络流等）转换为符合 Futures 标准的 `Stream`。通过这一转换，开发者可以使用流式处理方式（如 `StreamExt` 方法）异步逐块读取数据。

---

#### **关键组件**

1. **结构体定义**
   ```rust
   pub struct ReaderStream<R> {
       #[pin]
       reader: Option<R>,
       buf: BytesMut,
       capacity: usize,
   }
   ```
   - **`reader`**：保存实际的 `AsyncRead` 对象，当流结束时设为 `None`。
   - **`buf`**：使用 `BytesMut` 作为缓冲区，优化内存分配。
   - **`capacity`**：缓冲区的初始容量（默认 4096 字节）。

2. **构造函数**
   - **`new(reader: R)`**：使用默认缓冲区容量创建 `ReaderStream`。
   - **`with_capacity(reader: R, capacity: usize)`**：允许自定义初始缓冲区容量。

3. **Stream 实现**
   ```rust
   impl<R: AsyncRead> Stream for ReaderStream<R> {
       type Item = std::io::Result<Bytes>;
       fn poll_next(...)
   ```
   - **`poll_next`** 方法的核心逻辑：
     1. 检查 `reader` 是否存在，若已为 `None` 表示流结束。
     2. 确保缓冲区容量足够，不足时扩容至 `capacity`。
     3. 调用 `poll_read_buf` 从 `reader` 读取数据到缓冲区。
     4. 根据读取结果返回：
        - `Poll::Pending`：等待后续读取。
        - `Err`：读取失败，标记流结束。
        - `Ok(0)`：EOF，流结束。
        - `Ok(n)`：分割缓冲区内容为 `Bytes` 返回。

---

#### **工作原理**
- **适配逻辑**：通过 `poll_next` 将 `AsyncRead` 的 `read` 操作转换为流的 `next` 操作。
- **缓冲优化**：使用 `BytesMut` 缓冲区减少频繁分配，提升性能。
- **错误处理**：直接传递 `AsyncRead` 的错误，并标记流结束。
- **FusedStream**：流结束后不再产生新项，符合 `FusedStream` 行为。

---

#### **使用示例**
```rust
let data = b"hello, world!";
let mut stream = ReaderStream::new(&data[..]);
while let Some(chunk) = stream.next().await {
    stream_contents.extend_from_slice(&chunk?);
}
assert_eq!(stream_contents, data);
```
通过 `ReaderStream` 将字节数组转换为流，逐块读取并拼接数据。

---

#### **项目中的角色**