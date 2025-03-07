这个文件定义了 Tokio 运行时中标准错误输出（stderr）的异步写入句柄。

**主要组成部分：**

*   **`Stderr` 结构体：**
    *   这是一个结构体，代表标准错误输出的异步写入句柄。
    *   它包含一个 `std` 字段，类型为 `SplitByUtf8BoundaryIfWindows<Blocking<std::io::Stderr>>`。
        *   `std::io::Stderr` 是标准库中标准错误输出的句柄。
        *   `Blocking` 用于将同步的 `std::io::Stderr` 包装成异步的。
        *   `SplitByUtf8BoundaryIfWindows` 用于在 Windows 系统上按 UTF-8 边界分割写入，以避免潜在的输出问题。
*   **`stderr()` 函数：**
    *   这是一个公共函数，用于创建并返回一个 `Stderr` 实例。
    *   它首先调用 `std::io::stderr()` 获取标准库中的标准错误输出句柄。
    *   然后，使用 `Blocking::new()` 将同步的句柄包装成异步的。
    *   最后，使用 `SplitByUtf8BoundaryIfWindows::new()` 进一步包装，并创建一个 `Stderr` 实例返回。
*   **`AsRawFd` 和 `AsFd` trait 的实现 (仅限 Unix)：**
    *   针对 Unix 系统，实现了 `AsRawFd` 和 `AsFd` trait，允许获取标准错误输出的原始文件描述符。
*   **`AsRawHandle` 和 `AsHandle` trait 的实现 (仅限 Windows)：**
    *   针对 Windows 系统，实现了 `AsRawHandle` 和 `AsHandle` trait，允许获取标准错误输出的原始句柄。
*   **`AsyncWrite` trait 的实现：**
    *   `Stderr` 结构体实现了 `tokio::io::AsyncWrite` trait，这意味着它可以被用于异步写入数据。
    *   `poll_write()` 方法：将数据写入标准错误输出。
    *   `poll_flush()` 方法：刷新输出缓冲区。
    *   `poll_shutdown()` 方法：关闭写入流。

**功能：**

*   提供一个异步的接口，用于向标准错误输出写入数据。
*   处理了同步和异步之间的转换。
*   在 Windows 系统上处理了 UTF-8 边界问题。
*   提供了获取底层文件描述符或句柄的方法（针对 Unix 和 Windows）。

**与其他文件的关系：**

*   依赖于 `tokio::io` 模块，特别是 `AsyncWrite` trait 和 `blocking` 模块。
*   与 `stdio_common` 模块交互，用于处理 Windows 上的 UTF-8 边界。
*   与 `std::io` 模块交互，使用标准库中的标准错误输出句柄。
