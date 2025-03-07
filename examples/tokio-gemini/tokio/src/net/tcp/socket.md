这个文件定义了 `TcpSocket` 结构体，它是一个用于创建和配置 TCP 套接字的工具，在连接或监听之前使用。它允许用户设置套接字选项，例如重用地址、保持活动状态和延迟发送，并显式地绑定套接字到特定的地址。

关键组件：

*   `TcpSocket` 结构体：封装了底层的操作系统套接字，并提供了用于配置和操作套接字的方法。
*   `new_v4()` 和 `new_v6()` 方法：分别创建 IPv4 和 IPv6 的 `TcpSocket` 实例。
*   `set_keepalive()`、`keepalive()`、`set_reuseaddr()`、`reuseaddr()`、`set_reuseport()`、`reuseport()`、`set_send_buffer_size()`、`send_buffer_size()`、`set_recv_buffer_size()`、`recv_buffer_size()`、`set_linger()`、`linger()`、`set_nodelay()`、`nodelay()`、`set_tos()`、`tos()`、`bind_device()`、`device()` 方法：用于配置和获取套接字选项。
*   `local_addr()` 方法：获取套接字的本地地址。
*   `bind()` 方法：将套接字绑定到指定的地址。
*   `connect()` 方法：建立与指定地址的 TCP 连接，并返回一个 `TcpStream`。
*   `listen()` 方法：将套接字转换为 `TcpListener`，开始监听传入的连接。
*   `from_std_stream()` 方法：从 `std::net::TcpStream` 创建 `TcpSocket`。
*   `AsRawFd`、`AsFd`、`FromRawFd`、`IntoRawFd` (Unix) 和 `AsRawSocket`、`AsSocket`、`FromRawSocket`、`IntoRawSocket` (Windows) trait 实现：允许访问底层的原始文件描述符或套接字句柄，以便进行更底层的操作。
