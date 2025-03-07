这个文件定义了一个名为 `TcpListenerStream` 的结构体，它是一个对 `tokio::net::TcpListener` 的封装，实现了 `tokio_stream::Stream` trait。它的主要目的是将 `TcpListener` 适配成一个流，使得可以异步地接收来自 TCP 连接的输入。

**关键组件：**

*   **`TcpListenerStream` 结构体:**
    *   包含一个 `inner` 字段，类型为 `TcpListener`，用于持有底层的 TCP 监听器。
    *   实现了 `Debug` trait，方便调试。
    *   通过 `cfg_attr` 属性，在文档生成时，如果启用了 "net" 特性，则添加 `doc(cfg(feature = "net"))` 属性。
*   **`new` 方法:**
    *   创建一个新的 `TcpListenerStream` 实例，接收一个 `TcpListener` 作为参数。
*   **`into_inner` 方法:**
    *   获取内部的 `TcpListener`。
*   **`Stream` trait 的实现:**
    *   `type Item = io::Result<TcpStream>;`: 定义了流的每个元素是一个 `io::Result<TcpStream>`，表示接受到的 TCP 连接，或者在接受过程中发生的错误。
    *   `poll_next` 方法：
        *   这是 `Stream` trait 的核心方法，用于异步地尝试从监听器中接收新的 TCP 连接。
        *   调用 `self.inner.poll_accept(cx)` 来尝试接受连接。
        *   如果成功接受一个连接，则返回 `Poll::Ready(Some(Ok(stream)))`，其中 `stream` 是 `TcpStream`。
        *   如果发生错误，则返回 `Poll::Ready(Some(Err(err)))`。
        *   如果当前没有新的连接，则返回 `Poll::Pending`，表示稍后会再次尝试。
*   **`AsRef<TcpListener>` 和 `AsMut<TcpListener>` 的实现:**
    *   允许将 `TcpListenerStream` 转换为对内部 `TcpListener` 的引用，方便访问和修改底层的 TCP 监听器。

**与项目的关系：**

这个文件提供了一个工具，允许将 `tokio::net::TcpListener` 转换为一个 `Stream`，从而可以方便地使用 `tokio_stream` crate 提供的各种流处理功能，例如 `chain`、`filter` 等。这使得可以更简洁地编写异步 TCP 服务器，处理多个连接。
