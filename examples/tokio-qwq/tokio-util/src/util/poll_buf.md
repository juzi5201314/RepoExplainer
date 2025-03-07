### 文件说明：poll_buf.rs

#### 文件目的
该文件提供了两个核心函数 `poll_read_buf` 和 `poll_write_buf`，用于简化 Tokio 异步 I/O 操作中与缓冲区（`BufMut` 和 `Buf`）的交互。通过将 Tokio 的 `AsyncRead` 和 `AsyncWrite` 特性与 `bytes` crate 的缓冲区抽象结合，实现了高效且安全的异步读写操作。

---

#### 关键组件

1. **`poll_read_buf` 函数**
   - **功能**：从 `AsyncRead` 实现体中读取数据到 `BufMut` 缓冲区。
   - **实现细节**：
     - 检查缓冲区是否有剩余空间，若无则返回 `Poll::Ready(Ok(0))`。
     - 使用 `ReadBuf::uninit` 获取未初始化的内存空间，通过 `poll_read` 异步读取数据。
     - 确保读取后的内存区域有效，并通过 `unsafe` 块安全地更新缓冲区指针。
     - 返回实际读取的字节数。
   - **安全性**：通过断言确保内存指针一致性，避免未初始化内存的使用风险。

2. **`poll_write_buf` 函数**
   - **功能**：将 `Buf` 缓冲区的数据异步写入 `AsyncWrite` 实现体。
   - **实现细节**：
     - 检查缓冲区是否有剩余数据，若无则返回 `Poll::Ready(Ok(0))`。
     - 根据目标 `AsyncWrite` 是否支持向量写入（`poll_write_vectored`）：
       - 支持时：使用 `chunks_vectored` 将缓冲区拆分为多个 `IoSlice`。
       - 不支持时：直接使用单个 `chunk` 进行写入。
     - 写入完成后，更新缓冲区的读取指针。
   - **优化**：通过 `MAX_BUFS` 限制向量写入的切片数量，避免资源过度消耗。

---

#### 文件在项目中的角色