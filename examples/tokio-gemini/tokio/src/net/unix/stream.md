这个文件定义了 `UnixStream` 结构体，它代表一个已连接的 Unix 域套接字，并实现了 `AsyncRead` 和 `AsyncWrite` trait，使其可以与 Tokio 的异步 I/O 模型一起使用。

**主要组成部分：**

*   **`UnixStream` 结构体:**  封装了 `mio::net::UnixStream`，后者是底层非阻塞 Unix 域套接字的包装器。
*   **`connect` 方法:**  用于连接到指定的 Unix 域套接字路径。它处理了 Linux 和 Android 上的抽象套接字路径。
*   **`ready`、`readable`、`writable` 方法:**  用于等待套接字变为可读或可写状态。这些方法使用 `Interest` 枚举来指定感兴趣的事件。
*   **`poll_read_ready`、`poll_write_ready` 方法:**  用于轮询套接字是否准备好进行读写操作。
*   **`try_read`、`try_read_vectored`、`try_read_buf` 方法:**  尝试从套接字读取数据。这些方法是非阻塞的，如果套接字没有准备好，则返回 `WouldBlock` 错误。
*   **`try_write`、`try_write_vectored` 方法:**  尝试向套接字写入数据。这些方法也是非阻塞的，如果套接字没有准备好，则返回 `WouldBlock` 错误。
*   **`try_io`、`async_io` 方法:**  允许用户使用自定义的 IO 操作。
*   **`from_std` 方法:**  从标准库的 `std::os::unix::net::UnixStream` 创建 `UnixStream`。
*   **`into_std` 方法:**  将 `UnixStream` 转换为标准库的 `std::os::unix::net::UnixStream`。
*   **`pair` 方法:**  创建一个未命名的已连接的套接字对。
*   **`local_addr`、`peer_addr` 方法:**  分别返回本地和远程套接字地址。
*   **`peer_cred` 方法:**  返回对等进程的有效凭证。
*   **`take_error` 方法:**  获取并清除套接字的错误状态。
*   **`shutdown_std` 方法:**  关闭套接字的读、写或双向连接。
*   **`split`、`into_split` 方法:**  将 `UnixStream` 分割成读写两半，以便并发读写。
*   **`AsyncRead` 和 `AsyncWrite` 的实现:**  实现了 `AsyncRead` 和 `AsyncWrite` trait，允许使用 Tokio 的异步读写操作。

**与其他组件的交互：**

*   **`mio`:**  `UnixStream` 内部使用 `mio::net::UnixStream` 进行底层的非阻塞 I/O 操作。
*   **`tokio::io`:**  通过实现 `AsyncRead` 和 `AsyncWrite` trait，`UnixStream` 与 Tokio 的异步 I/O 模型集成。
*   **`tokio::net::unix::split` 和 `tokio::net::unix::split_owned`:**  提供了将 `UnixStream` 分割成读写两半的功能，以支持并发操作。
*   **`tokio::net::unix::SocketAddr`:**  用于表示 Unix 域套接字地址。
*   **`tokio::net::unix::ucred`:**  用于获取对等进程的凭证。
