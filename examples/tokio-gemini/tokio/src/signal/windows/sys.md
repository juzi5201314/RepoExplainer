这个文件实现了在 Windows 操作系统上处理控制台信号的功能，特别是处理像 Ctrl+C、Ctrl+Break、关机、注销等事件。

**主要组成部分：**

*   **`ctrl_*` 函数：** 这些函数（`ctrl_break`、`ctrl_close`、`ctrl_c`、`ctrl_logoff`、`ctrl_shutdown`）是公共 API，用于创建监听特定控制台事件的 `RxFuture`。它们内部调用 `new` 函数来注册监听器。
*   **`new` 函数：**  这个函数负责初始化全局状态（如果尚未初始化），并使用全局注册表（`globals()`）注册一个监听器，用于接收特定事件的通知。它返回一个 `RxFuture`，用于异步接收信号。
*   **`event_requires_infinite_sleep_in_handler` 函数：**  此函数判断某个事件的处理程序是否需要无限循环。对于某些事件（如 `CTRL_CLOSE_EVENT`、`CTRL_LOGOFF_EVENT`、`CTRL_SHUTDOWN_EVENT`），处理程序立即返回会导致进程终止，因此需要无限循环来阻止这种情况。
*   **`OsStorage` 结构体和 `Init`、`Storage` trait 的实现：**  `OsStorage` 结构体存储了关于每个控制台事件的信息。`Init` trait 用于初始化 `OsStorage`，而 `Storage` trait 定义了访问和操作事件信息的方法。
*   **`OsExtraData` 结构体和 `Init` trait 的实现：**  `OsExtraData` 结构体用于存储额外的操作系统相关数据，并实现了 `Init` trait。
*   **`global_init` 函数：**  这个函数使用 `Once` 来确保只初始化一次控制台处理程序。它调用 `SetConsoleCtrlHandler` Windows API 来设置一个处理程序函数，用于接收控制台事件。
*   **`handler` 函数：**  这是一个由 Windows 操作系统调用的回调函数，用于处理控制台事件。它将事件 ID 记录到全局注册表中，并广播事件。如果事件被处理并且需要无限循环，它会进入一个无限循环。
*   **`tests` 模块：**  包含单元测试，用于验证控制台信号处理的正确性。测试模拟了 Windows 事件的触发，并验证了 `RxFuture` 是否正确接收到信号。

**工作流程：**

1.  当用户调用 `ctrl_*` 函数时，会创建一个 `RxFuture`，用于异步接收信号。
2.  `new` 函数会调用 `global_init` 函数，确保控制台处理程序已初始化。
3.  `global_init` 函数会调用 `SetConsoleCtrlHandler` 设置一个 `handler` 函数。
4.  当 Windows 操作系统检测到控制台事件（例如，用户按下 Ctrl+C）时，它会调用 `handler` 函数。
5.  `handler` 函数将事件 ID 记录到全局注册表中，并广播事件。
6.  `RxFuture` 接收到事件广播后，会变为就绪状态，允许用户处理信号。

**与其他部分的关联：**

*   **`crate::signal::registry` 模块：**  这个模块提供了全局注册表，用于存储和管理信号监听器。
*   **`crate::signal::RxFuture`：**  这是一个异步接收器，用于接收控制台信号。
*   **`windows-sys` crate：**  这个 crate 提供了 Windows API 的绑定，用于与 Windows 操作系统交互。
*   **`tokio` 运行时：**  这个文件中的代码是为 `tokio` 运行时设计的，用于在异步环境中处理控制台信号。
