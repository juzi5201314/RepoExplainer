这个文件定义了 `SyncIoBridge` 结构体，它允许将 `tokio::io` 中的异步 I/O 操作同步地用作 `std::io` 中的同步 I/O 操作。

**主要组件：**

*   **`SyncIoBridge<T>` 结构体：**
    *   `src: T`： 包含一个实现了 `tokio::io::AsyncRead`、`AsyncWrite`、`AsyncSeek` 和 `AsyncBufRead` 特征的异步 I/O 对象。
    *   `rt: tokio::runtime::Handle`： 存储当前 Tokio 运行时句柄，用于在同步 I/O 操作中调用 `block_on`。
*   **`impl` 块：**
    *   为 `SyncIoBridge` 实现了 `std::io` 中的 `Read`、`Write`、`Seek` 和 `BufRead` 特征。这些实现通过在 Tokio 运行时上调用 `block_on` 来同步地执行异步 I/O 操作。
    *   提供了 `new` 和 `new_with_handle` 构造函数，用于创建 `SyncIoBridge` 实例。`new` 函数使用当前线程的 Tokio 运行时句柄，而 `new_with_handle` 允许指定一个自定义的运行时句柄。
    *   提供了 `into_inner` 方法，用于获取底层的异步 I/O 对象。
    *   提供了 `is_write_vectored` 方法，用于判断底层的 `AsyncWrite` 是否支持向量写。
    *   提供了 `shutdown` 方法，用于关闭写入器。
    *   实现了 `AsMut` 和 `AsRef` 特征，方便访问底层的异步 I/O 对象。

**工作原理：**

`SyncIoBridge` 的核心在于它将异步 I/O 操作转换为同步操作。它通过在 `std::io` 特征的实现中使用 `tokio::runtime::Handle::block_on` 来实现这一点。当调用 `read`、`write` 等方法时，`SyncIoBridge` 会使用存储的 Tokio 运行时句柄来阻塞当前线程，直到异步 I/O 操作完成。

**使用场景和注意事项：**

*   **同步 I/O 接口：** 当需要将异步 I/O 对象与需要同步 I/O 接口的库或代码集成时，可以使用 `SyncIoBridge`。
*   **`spawn_blocking`：** 推荐在 `tokio::task::spawn_blocking` 任务中使用 `SyncIoBridge`，以避免阻塞异步运行时。
*   **性能影响：** 使用 `SyncIoBridge` 会阻塞线程，可能导致性能下降。在可能的情况下，应尽量避免使用它，并考虑使用异步 I/O 操作。
*   **运行时上下文：** `SyncIoBridge` 必须在 Tokio 运行时上下文中使用。

**代码示例：**

该文件包含多个代码示例，展示了如何使用 `SyncIoBridge` 以及何时应该避免使用它。这些示例涵盖了哈希数据、压缩数据和解析数据格式等场景。
