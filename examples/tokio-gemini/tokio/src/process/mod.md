这段代码文件实现了 Tokio 异步进程管理模块。

**主要功能：**

*   **异步进程创建和管理：** 提供了 `Command` 结构体，它模仿了标准库 `std::process::Command` 的接口，但提供了异步版本的进程创建函数，例如 `spawn`、`status` 和 `output`。这些函数返回与 Tokio 兼容的 "future-aware" 类型。
*   **跨平台支持：** 通过在 Unix 上进行信号处理和在 Windows 上使用系统 API 来实现异步进程支持。
*   **I/O 重定向：** 允许配置子进程的标准输入、标准输出和标准错误，支持管道、继承等方式。
*   **进程控制：** 提供了 `kill_on_drop` 选项，用于控制在 `Child` 句柄被丢弃时是否杀死子进程。
*   **示例代码：** 提供了多个示例，展示了如何使用 `Command` 结构体来创建、等待、获取输出、以及通过管道进行 I/O 重定向。

**关键组件：**

*   **`Command` 结构体：**  类似于 `std::process::Command`，用于构建和配置要执行的进程。它包含进程的程序路径、参数、环境变量、工作目录以及 I/O 重定向配置等。
*   **`Child` 结构体：**  表示一个已创建的子进程。它提供了获取子进程 ID、获取 I/O 流句柄（`stdin`、`stdout`、`stderr`）、等待子进程结束（`wait`）、杀死子进程（`kill`）等方法。
*   **`ChildStdin`、`ChildStdout`、`ChildStderr` 结构体：**  分别表示子进程的标准输入、标准输出和标准错误流。它们实现了 `AsyncRead` 和 `AsyncWrite` trait，允许异步地与子进程进行 I/O 操作。
*   **`FusedChild` 枚举：** 用于跟踪子进程的状态，包括 `Child` (子进程仍在运行) 和 `Done` (子进程已完成)。
*   **`ChildDropGuard` 结构体：** 用于在 `Child` 被丢弃时，根据 `kill_on_drop` 的设置决定是否杀死子进程。

**与其他组件的关联：**

*   **`tokio::process` 模块：**  该文件是 `tokio::process` 模块的一部分，提供了异步进程管理的核心功能。
*   **`tokio::io` 模块：**  `ChildStdin`、`ChildStdout` 和 `ChildStderr` 使用 `tokio::io` 模块的 `AsyncRead` 和 `AsyncWrite` trait，实现异步 I/O。
*   **`std::process::Command`：** `Command` 结构体模仿了 `std::process::Command` 的 API，提供了类似的功能，但进行了异步化处理。
*   **Tokio Runtime：**  该文件中的代码依赖于 Tokio 运行时，用于执行异步任务和管理 I/O 操作。

**总结：**

该文件定义了 Tokio 异步进程管理的核心组件，允许用户以异步方式创建、控制和与子进程进行交互。它提供了类似于标准库 `std::process::Command` 的 API，并与 Tokio 的异步运行时和 I/O 模型紧密集成。
