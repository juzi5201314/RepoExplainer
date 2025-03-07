这个文件实现了在 Windows 操作系统上异步处理子进程的功能。它主要关注如何监控子进程的退出，以及如何处理子进程的标准输入、输出和错误流。

**主要组件：**

*   **`Child` 结构体：** 封装了 `std::process::Child`，并添加了用于异步等待子进程退出的逻辑。它包含一个 `StdChild` 实例和一个 `Waiting` 结构体的 `Option`，用于跟踪等待操作的状态。
*   **`Waiting` 结构体：** 存储了用于等待子进程退出的信息，包括一个 `oneshot::Receiver` 用于接收退出信号，一个 Windows 句柄 (`wait_object`) 用于注册等待，以及一个指向 `oneshot::Sender` 的指针。
*   **`ChildStdio` 结构体：** 封装了子进程的标准输入/输出/错误流，使其可以异步读写。它包含一个 `Arc<StdFile>` 用于访问原始句柄，以及一个 `Blocking<ArcFile>` 用于异步 I/O 操作。
*   **`spawn_child` 函数：** 负责创建子进程，并处理标准输入/输出/错误流。它使用 `std::process::Command` 来启动子进程，并将标准流转换为 `ChildStdio` 类型，以便进行异步操作。
*   **`Child` 的 `Future` 实现：** 实现了 `Future` trait，允许异步等待子进程的退出。它使用 `RegisterWaitForSingleObject` 函数在 Windows 线程池中注册一个等待操作，当子进程退出时，会触发一个回调函数，该回调函数会通过 `oneshot` 发送一个信号，从而唤醒等待的 future。
*   **`ChildStdio` 的 `AsyncRead` 和 `AsyncWrite` 实现：** 实现了 `AsyncRead` 和 `AsyncWrite` trait，允许异步读写子进程的标准输入/输出/错误流。它使用 `Blocking` 结构体来包装 `ArcFile`，从而在异步环境中执行 I/O 操作。
*   **`callback` 函数：** 这是一个 Windows 回调函数，当子进程退出时被调用。它负责通过 `oneshot` 发送一个信号，通知等待的 future。
*   **`stdio` 函数：** 将 `std::process::Stdio` 转换为 `ChildStdio`，以便进行异步操作。
*   **`convert_to_file` 和 `convert_to_stdio` 函数：** 用于在 `ChildStdio` 和 `std::process::Stdio` 之间进行转换。
*   **`duplicate_handle` 函数：** 用于复制一个 Windows 句柄。

**工作流程：**

1.  **子进程创建：** `spawn_child` 函数使用 `std::process::Command` 创建子进程，并获取其标准输入/输出/错误流。
2.  **异步等待：** `Child` 的 `Future` 实现通过 `RegisterWaitForSingleObject` 在 Windows 线程池中注册一个等待操作，等待子进程退出。
3.  **信号通知：** 当子进程退出时，Windows 会触发 `callback` 函数。`callback` 函数通过 `oneshot` 发送一个信号，通知等待的 future。
4.  **结果处理：** `Child` 的 `poll` 方法会检查 `oneshot` 的接收端，如果收到信号，则表示子进程已经退出，并返回退出状态。
5.  **异步 I/O：** `ChildStdio` 结构体允许异步读写子进程的标准输入/输出/错误流。

**与其他部分的关联：**

*   它与 `crate::process` 模块中的其他文件协同工作，提供了创建、管理和监控子进程的完整功能。
*   它使用了 `tokio::sync::oneshot` 用于进程退出信号的传递。
*   它使用了 `crate::io` 模块中的异步 I/O trait 和相关结构体，实现了异步读写子进程的标准输入/输出/错误流。
*   它使用了 Windows API 函数，如 `RegisterWaitForSingleObject` 和 `DuplicateHandle`，来实现进程等待和句柄复制。
