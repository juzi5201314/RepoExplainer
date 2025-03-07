这个文件定义了两个结构体 `CtrlCStream` 和 `CtrlBreakStream`，它们是 `tokio::signal::windows` 模块中 `CtrlC` 和 `CtrlBreak` 的包装器，实现了 `tokio_stream::Stream` trait。 这使得可以像处理其他流一样处理 Windows 上的 Ctrl+C 和 Ctrl+Break 信号。

**关键组件：**

*   **`CtrlCStream`**:
    *   包装了 `tokio::signal::windows::CtrlC`，用于处理 Ctrl+C 信号。
    *   实现了 `Stream` trait，`Item` 类型为 `()`，表示每次收到信号时产生一个空值。
    *   `poll_next` 方法调用了内部 `CtrlC` 的 `poll_recv` 方法来检查是否收到了 Ctrl+C 信号。
    *   提供了 `new` 和 `into_inner` 方法，用于创建和获取内部的 `CtrlC` 实例。
    *   实现了 `AsRef` 和 `AsMut` trait，方便访问和修改内部的 `CtrlC` 实例。
*   **`CtrlBreakStream`**:
    *   包装了 `tokio::signal::windows::CtrlBreak`，用于处理 Ctrl+Break 信号。
    *   实现了 `Stream` trait，`Item` 类型为 `()`，表示每次收到信号时产生一个空值。
    *   `poll_next` 方法调用了内部 `CtrlBreak` 的 `poll_recv` 方法来检查是否收到了 Ctrl+Break 信号。
    *   提供了 `new` 和 `into_inner` 方法，用于创建和获取内部的 `CtrlBreak` 实例。
    *   实现了 `AsRef` 和 `AsMut` trait，方便访问和修改内部的 `CtrlBreak` 实例。

**如何融入项目：**

这两个结构体允许开发者使用 `tokio_stream` 库来异步地处理 Windows 上的 Ctrl+C 和 Ctrl+Break 信号。 它们将底层的信号处理机制封装成一个流，可以与其他流操作结合使用，例如使用 `StreamExt` trait 的方法进行过滤、映射等操作。 这使得在 Windows 环境下构建响应 Ctrl+C 和 Ctrl+Break 信号的应用程序变得更加容易和灵活。
