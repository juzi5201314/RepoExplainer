这个文件定义了 `TcpListener` 结构体，它代表一个 TCP 监听器，用于接受传入的 TCP 连接。它提供了绑定到地址、接受连接、获取本地地址和设置/获取 TTL 等功能。

**关键组件：**

*   **`TcpListener` 结构体：**
    *   包含一个 `PollEvented<mio::net::TcpListener>` 成员 `io`，用于处理底层 I/O 操作。`PollEvented` 封装了 `mio` 的 `TcpListener`，使其与 Tokio 的异步运行时兼容。
*   **`bind` 方法：**
    *   用于将 `TcpListener` 绑定到指定的地址。它接受一个实现了 `ToSocketAddrs` trait 的地址参数，并尝试绑定到该地址。如果绑定失败，它会尝试其他地址，直到成功或所有地址都失败。
    *   设置 `SO_REUSEADDR` 选项。
*   **`accept` 方法：**
    *   异步地接受新的传入连接。它会等待新的 TCP 连接建立，然后返回一个 `TcpStream` 和远程对端的地址。
    *   使用 `async_io` 方法来异步地执行 I/O 操作，并处理潜在的错误。
*   **`poll_accept` 方法：**
    *   轮询接受新的传入连接。如果当前没有连接可接受，则返回 `Poll::Pending`。
*   **`from_std` 方法：**
    *   从标准库的 `std::net::TcpListener` 创建一个 `TcpListener`。这允许将现有的标准库监听器包装到 Tokio 的异步环境中。
    *   需要确保传入的 `TcpListener` 处于非阻塞模式。
*   **`into_std` 方法：**
    *   将 Tokio 的 `TcpListener` 转换为标准库的 `std::net::TcpListener`。
*   **`local_addr` 方法：**
    *   返回监听器绑定的本地地址。
*   **`ttl` 方法：**
    *   获取 `IP_TTL` 选项的值。
*   **`set_ttl` 方法：**
    *   设置 `IP_TTL` 选项的值。
*   **`TryFrom<net::TcpListener> for TcpListener` trait 实现：**
    *   允许使用 `try_from` 方法将 `std::net::TcpListener` 转换为 `TcpListener`。
*   **`Debug` trait 实现：**
    *   允许使用 `{:?}` 格式化输出 `TcpListener`。
*   **`sys` 模块 (针对 Unix, WASI 和 Windows)：**
    *   实现了 `AsRawFd` (Unix, WASI) 和 `AsRawSocket` (Windows) trait，允许访问底层的原始文件描述符或套接字。
    *   实现了 `AsFd` (Unix, WASI) 和 `AsSocket` (Windows) trait，允许使用 `BorrowedFd` 和 `BorrowedSocket`。

**与其他组件的关联：**

*   与 `TcpStream` 配合使用，`TcpStream` 代表一个 TCP 连接。`TcpListener` 的 `accept` 方法返回 `TcpStream`。
*   与 `mio` 库交互，`mio` 库提供了底层的非阻塞 I/O 支持。
*   与 `tokio::net` 模块的其他组件（如 `to_socket_addrs`）协同工作，用于网络地址解析和处理。
*   实现了 `Stream` trait，允许使用 `TcpListener` 作为异步流。
