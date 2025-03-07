这个文件定义了 `TcpStream` 结构体，它是 Tokio 框架中用于 TCP 连接的核心组件。它提供了异步读写操作，并封装了底层操作系统提供的 TCP 套接字。

**主要组成部分：**

*   **`cfg_not_wasi!` 宏：**  根据编译配置，条件性地包含与 WASI (WebAssembly System Interface) 相关的代码。
*   **`use` 语句：** 引入了 Tokio 框架中其他模块和标准库中的相关类型，例如 `AsyncRead`, `AsyncWrite`, `Interest`, `PollEvented`, `SocketAddr` 等，这些类型用于实现异步 I/O 操作、处理网络地址等。
*   **`TcpStream` 结构体：**  核心结构体，封装了 `mio::net::TcpStream`，后者是底层非阻塞 TCP 套接字的包装。`TcpStream` 实现了 `AsyncRead` 和 `AsyncWrite` trait，从而支持异步读写操作。
*   **`impl TcpStream` 块：**  实现了 `TcpStream` 的各种方法，包括：
    *   **`connect` 方法：**  异步建立到远程主机的 TCP 连接。它处理了地址解析和连接建立的流程。
    *   **`from_std` 方法：**  从标准库的 `std::net::TcpStream` 创建 `TcpStream`。这允许将现有的阻塞 TCP 流转换为 Tokio 的异步流。
    *   **`into_std` 方法：**  将 Tokio 的 `TcpStream` 转换为标准库的 `std::net::TcpStream`。
    *   **`local_addr` 和 `peer_addr` 方法：**  分别获取本地和远程的套接字地址。
    *   **`poll_peek` 方法：**  尝试从套接字接收数据，但不从队列中移除数据。
    *   **`ready`, `readable`, `writable` 方法：**  用于等待套接字变为可读或可写状态。
    *   **`poll_read_ready`, `poll_write_ready` 方法：**  检查套接字是否准备好进行读写操作。
    *   **`try_read`, `try_read_vectored`, `try_read_buf` 方法：**  尝试从套接字读取数据，如果套接字未准备好，则返回 `WouldBlock` 错误。
    *   **`try_write`, `try_write_vectored` 方法：**  尝试向套接字写入数据，如果套接字未准备好，则返回 `WouldBlock` 错误。
    *   **`try_io`, `async_io` 方法：**  允许用户自定义 I/O 操作。
    *   **`peek` 方法：**  从套接字接收数据，但不从队列中移除数据。
    *   **`shutdown_std` 方法：**  关闭连接的读、写或双向通道。
    *   **`nodelay`, `set_nodelay` 方法：**  控制 TCP_NODELAY 选项。
    *   **`linger`, `set_linger` 方法：**  控制 SO_LINGER 选项。
    *   **`ttl`, `set_ttl` 方法：**  控制 IP_TTL 选项。
    *   **`split`, `into_split` 方法：**  将 `TcpStream` 分割成读写两部分，允许并发读写。
    *   **`poll_read_priv`, `poll_write_priv`, `poll_write_vectored_priv` 方法：**  内部使用的轮询 I/O 方法。
*   **`impl TryFrom<std::net::TcpStream> for TcpStream` 块：**  实现了 `TryFrom` trait，允许从标准库的 `TcpStream` 转换到 Tokio 的 `TcpStream`。
*   **`impl AsyncRead for TcpStream` 和 `impl AsyncWrite for TcpStream` 块：**  实现了 `AsyncRead` 和 `AsyncWrite` trait，使得 `TcpStream` 可以进行异步读写操作。
*   **`impl fmt::Debug for TcpStream` 块：**  实现了 `Debug` trait，方便调试。
*   **`cfg_unix!`, `cfg_windows!`, `cfg_all(tokio_unstable, target_os = "wasi")` 模块：**  根据不同的操作系统，实现 `AsRawFd`, `AsFd`, `AsRawSocket`, `AsSocket` trait，用于获取底层的文件描述符或套接字句柄。

**与其他组件的交互：**

*   **`crate::net` 模块：**  `TcpStream` 属于 `crate::net` 模块，该模块提供了网络相关的抽象。
*   **`crate::io` 模块：**  `TcpStream` 实现了 `AsyncRead` 和 `AsyncWrite` trait，这些 trait 定义在 `crate::io` 模块中，用于异步 I/O 操作。
*   **`mio::net::TcpStream`：**  `TcpStream` 内部封装了 `mio::net::TcpStream`，后者是底层非阻塞 TCP 套接字的包装，负责实际的 I/O 操作。
*   **`PollEvented`：**  `TcpStream` 使用 `PollEvented` 来管理底层套接字的就绪状态，并与 Tokio 的事件循环集成。
*   **`split` 和 `split_owned`：**  用于将 `TcpStream` 分割成读写两部分，方便并发操作。

**总结：**

这个文件定义了 `TcpStream`，它是 Tokio 框架中用于 TCP 连接的核心组件，提供了异步读写操作，并封装了底层操作系统提供的 TCP 套接字。
