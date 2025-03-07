这个文件实现了 `UnixStream` 的分割功能，允许将一个 `UnixStream` 分割成一个只读的 `ReadHalf` 和一个只写的 `WriteHalf`。这种分割方式避免了额外的开销，并在类型级别强制执行所有不变性。

**关键组件：**

*   **`ReadHalf<'a>(&'a UnixStream)`**:  表示 `UnixStream` 的只读部分。它借用了对原始 `UnixStream` 的引用。
*   **`WriteHalf<'a>(&'a UnixStream)`**:  表示 `UnixStream` 的只写部分。它也借用了对原始 `UnixStream` 的引用。
*   **`split(stream: &mut UnixStream) -> (ReadHalf<'_>, WriteHalf<'_>)`**:  这个函数是分割的核心。它接收一个可变的 `UnixStream` 引用，并返回一个 `ReadHalf` 和一个 `WriteHalf` 的元组。
*   **`ReadHalf` 的方法**:
    *   `ready()`:  等待指定的就绪状态（例如，可读）。
    *   `readable()`:  等待套接字变得可读。
    *   `try_read()`:  尝试从流中读取数据到缓冲区。
    *   `try_read_buf()`:  尝试从流中读取数据到 `bytes::BufMut` 缓冲区（如果启用了 `cfg_io_util` 特性）。
    *   `try_read_vectored()`:  尝试从流中读取数据到多个缓冲区。
    *   `peer_addr()`:  获取连接的远程地址。
    *   `local_addr()`:  获取连接的本地地址。
*   **`WriteHalf` 的方法**:
    *   `ready()`:  等待指定的就绪状态（例如，可写）。
    *   `writable()`:  等待套接字变得可写。
    *   `try_write()`:  尝试将缓冲区写入流。
    *   `try_write_vectored()`:  尝试将多个缓冲区写入流。
    *   `peer_addr()`:  获取连接的远程地址。
    *   `local_addr()`:  获取连接的本地地址。
*   **`AsyncRead` 和 `AsyncWrite` 的实现**:  `ReadHalf` 实现了 `AsyncRead` trait，允许异步读取数据。`WriteHalf` 实现了 `AsyncWrite` trait，允许异步写入数据。`poll_shutdown` 方法用于关闭写方向的 `UnixStream`。
*   **`AsRef<UnixStream>` 的实现**:  `ReadHalf` 和 `WriteHalf` 都实现了 `AsRef<UnixStream>`，允许将它们转换为对原始 `UnixStream` 的引用。

**与其他组件的交互：**

*   这个文件与 `UnixStream` 密切相关，它提供了分割 `UnixStream` 的功能。
*   它使用了 `crate::io` 模块中的 `AsyncRead`、`AsyncWrite`、`Interest`、`ReadBuf` 和 `Ready` trait 和结构体。
*   它使用了 `crate::net` 模块中的 `UnixStream` 和 `SocketAddr`。
*   如果启用了 `cfg_io_util` 特性，它会使用 `bytes::BufMut`。
