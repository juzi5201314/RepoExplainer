这个文件定义了 `TcpStream` 的读写半部分，允许将一个 `TcpStream` 分割成独立的读和写句柄，从而实现并发的读写操作。

**主要组成部分：**

*   **`ReadHalf<'a>`**:  代表 `TcpStream` 的只读部分。它实现了 `AsyncRead` trait，允许异步读取数据。它持有对原始 `TcpStream` 的借用，确保了数据一致性。
*   **`WriteHalf<'a>`**: 代表 `TcpStream` 的只写部分。它实现了 `AsyncWrite` trait，允许异步写入数据。同样，它也持有对原始 `TcpStream` 的借用。
*   **`split(stream: &mut TcpStream) -> (ReadHalf<'_>, WriteHalf<'_>)`**:  这个函数将一个可变的 `TcpStream` 分割成 `ReadHalf` 和 `WriteHalf`。它创建了两个分别指向原始 `TcpStream` 的借用，并返回这两个半部分。
*   **`impl ReadHalf<'_>`**:  为 `ReadHalf` 提供了各种异步读取方法，如 `poll_peek`, `peek`, `ready`, `readable`, `try_read`, `try_read_vectored` 和 `try_read_buf` (如果启用了 `cfg_io_util`)。这些方法都通过调用底层的 `TcpStream` 的相应方法来实现实际的读取操作。此外，还提供了 `peer_addr` 和 `local_addr` 方法来获取连接的地址信息。
*   **`impl WriteHalf<'_>`**:  为 `WriteHalf` 提供了各种异步写入方法，如 `ready`, `writable`, `try_write`, `try_write_vectored`。这些方法都通过调用底层的 `TcpStream` 的相应方法来实现实际的写入操作。`poll_flush` 是一个空操作，因为 TCP 的 flush 是一个 no-op。`poll_shutdown` 关闭了写方向的流。此外，还提供了 `peer_addr` 和 `local_addr` 方法来获取连接的地址信息。
*   **`impl AsyncRead for ReadHalf<'_>`**:  实现了 `AsyncRead` trait，通过调用底层 `TcpStream` 的 `poll_read_priv` 方法来异步读取数据。
*   **`impl AsyncWrite for WriteHalf<'_>`**:  实现了 `AsyncWrite` trait，通过调用底层 `TcpStream` 的 `poll_write_priv`, `poll_write_vectored_priv`, `is_write_vectored`, `poll_flush` 和 `poll_shutdown` 方法来异步写入数据。
*   **`impl AsRef<TcpStream> for ReadHalf<'_>` 和 `impl AsRef<TcpStream> for WriteHalf<'_>`**:  允许将 `ReadHalf` 和 `WriteHalf` 转换为对 `TcpStream` 的引用。

**功能和作用：**

这个文件提供了将 `TcpStream` 分割成读写两半的功能，使得可以并发地从一个 TCP 连接中读取数据和写入数据。这对于需要同时进行读写操作的应用程序非常有用，例如服务器端处理多个客户端连接。通过将读写操作分离，可以避免阻塞，提高程序的并发性能。
