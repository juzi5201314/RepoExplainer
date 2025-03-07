这个文件实现了 `UnixStream` 的所有权分割支持。它允许将一个 `UnixStream` 分割成 `OwnedReadHalf` 和 `OwnedWriteHalf`，分别实现 `AsyncRead` 和 `AsyncWrite` trait。这种分割方式与通用的 `AsyncRead + AsyncWrite` 分割相比，没有额外的开销，并在类型级别强制执行所有不变性。

主要组件：

*   **`OwnedReadHalf`**:  表示 `UnixStream` 的所有权读取半部分。它实现了 `AsyncRead` trait，允许异步读取数据。
*   **`OwnedWriteHalf`**: 表示 `UnixStream` 的所有权写入半部分。它实现了 `AsyncWrite` trait，允许异步写入数据。`poll_shutdown` 方法会关闭流的写入方向。丢弃 `OwnedWriteHalf` 也会关闭流的写入方向。
*   **`split_owned(stream: UnixStream) -> (OwnedReadHalf, OwnedWriteHalf)`**:  将一个 `UnixStream` 分割成 `OwnedReadHalf` 和 `OwnedWriteHalf`。它创建了两个 `Arc` 引用来共享底层的 `UnixStream`。
*   **`reunite(read: OwnedReadHalf, write: OwnedWriteHalf) -> Result<UnixStream, ReuniteError>`**: 尝试将 `OwnedReadHalf` 和 `OwnedWriteHalf` 重新组合成原始的 `UnixStream`。只有当这两个半部分来自同一个 `UnixStream` 的分割时，才能成功。
*   **`ReuniteError`**:  一个错误类型，表示尝试重新组合来自不同 socket 的半部分失败。

该文件定义了 `OwnedReadHalf` 和 `OwnedWriteHalf` 的各种方法，包括：

*   `ready()`: 等待指定的就绪状态。
*   `readable()`: 等待可读状态。
*   `writable()`: 等待可写状态。
*   `try_read()`: 尝试从流中读取数据。
*   `try_write()`: 尝试向流中写入数据。
*   `peer_addr()`: 获取远程地址。
*   `local_addr()`: 获取本地地址。
*   `forget()`: 销毁写入半部分，但不关闭写入方向，直到读取半部分被丢弃。

该文件通过实现 `AsyncRead` 和 `AsyncWrite` trait，使得 `OwnedReadHalf` 和 `OwnedWriteHalf` 可以分别用于异步读取和写入操作。
