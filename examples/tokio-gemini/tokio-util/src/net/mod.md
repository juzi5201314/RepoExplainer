这个文件定义了用于 Tokio 的网络辅助工具，主要关注 TCP、UDP 和 Unix 相关的操作。

**主要组成部分：**

1.  **`Listener` 特征：**
    *   定义了一个通用的监听器接口，用于 `TcpListener` 和 `UnixListener`。
    *   `Io` 关联类型：表示监听器产生的流的类型，例如 `TcpStream` 或 `UnixStream`。
    *   `Addr` 关联类型：表示监听器的地址类型，例如 `SocketAddr` 或 `unix::SocketAddr`。
    *   `poll_accept()` 方法：轮询以接受来自监听器的新传入连接。
    *   `accept()` 方法：接受来自监听器的新传入连接，返回一个 `ListenerAcceptFut` future。
    *   `local_addr()` 方法：返回监听器绑定的本地地址。

2.  **`ListenerAcceptFut` 结构体：**
    *   一个 future，用于异步地接受来自监听器的连接。
    *   实现了 `Future` 特征，在 `poll()` 方法中调用底层监听器的 `poll_accept()` 方法。

3.  **`impl Listener for tokio::net::TcpListener`：**
    *   为 `tokio::net::TcpListener` 实现了 `Listener` 特征。
    *   将 `TcpListener` 的 `poll_accept()` 和 `local_addr()` 方法适配到 `Listener` 特征。

4.  **`impl<L, R> Either<L, R> where L: Listener, R: Listener`：**
    *   为 `Either` 枚举（可能来自 crate::either 模块）实现了 `accept()` 和 `local_addr()` 方法，允许同时处理两种类型的监听器（例如，TCP 和 Unix）。
    *   `accept()` 方法：根据 `Either` 的变体，调用相应监听器的 `accept()` 方法，并返回一个 `Either` 包含结果。
    *   `local_addr()` 方法：根据 `Either` 的变体，调用相应监听器的 `local_addr()` 方法，并返回一个 `Either` 包含地址。

5.  **`#[cfg(unix)] pub mod unix;`：**
    *   条件编译模块，如果目标平台是 Unix，则包含 `unix` 模块。这个模块很可能包含与 Unix 域套接字相关的特定实现。

**作用：**
