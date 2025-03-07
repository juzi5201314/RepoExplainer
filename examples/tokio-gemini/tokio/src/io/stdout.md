这个文件定义了 `Stdout` 结构体，它是一个 Tokio 异步标准输出流的句柄。它允许在 Tokio 运行时中向标准输出写入数据。

**关键组件：**

*   **`Stdout` 结构体**:
    *   `std`: 包含一个 `SplitByUtf8BoundaryIfWindows` 包装的 `Blocking<std::io::Stdout>`。`Blocking` 用于在 Tokio 运行时中处理阻塞的 I/O 操作，`SplitByUtf8BoundaryIfWindows` 确保在 Windows 系统上按照 UTF-8 边界分割写入，以避免出现问题。
*   **`stdout()` 函数**:
    *   创建一个新的 `Stdout` 实例，它包装了标准输出流 `std::io::stdout()`。
    *   使用 `Blocking` 包装标准输出流，以便在 Tokio 运行时中使用。
    *   使用 `SplitByUtf8BoundaryIfWindows` 包装 `Blocking` 实例。
*   **`AsRawFd` 和 `AsFd` trait 的实现 (仅限 Unix)**:
    *   为 `Stdout` 实现了 `AsRawFd` 和 `AsFd` trait，允许获取底层文件描述符。
*   **`AsRawHandle` 和 `AsHandle` trait 的实现 (仅限 Windows)**:
    *   为 `Stdout` 实现了 `AsRawHandle` 和 `AsHandle` trait，允许获取底层句柄。
*   **`AsyncWrite` trait 的实现**:
    *   为 `Stdout` 实现了 `AsyncWrite` trait，允许异步写入数据。
    *   `poll_write`：将写入操作委托给内部的 `std` 字段。
    *   `poll_flush`：将刷新操作委托给内部的 `std` 字段。
    *   `poll_shutdown`：将关闭操作委托给内部的 `std` 字段。

**功能和作用：**

*   提供一个异步的、线程安全的标准输出流句柄。
*   允许在 Tokio 运行时中异步地写入数据到标准输出。
*   处理 Windows 上的 UTF-8 边界问题。
*   提供底层文件描述符或句柄的访问，以便与其他系统调用或库进行交互。

**与项目的关系：**

这个文件是 Tokio I/O 模块的一部分，它提供了异步 I/O 操作的实现。`Stdout` 结构体允许程序将数据异步地写入标准输出，这对于构建异步应用程序至关重要。
