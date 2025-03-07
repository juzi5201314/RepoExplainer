这个文件 (`mod.rs`) 实现了在 Unix 系统上处理子进程的功能，是 `tokio` 库中 `process` 模块的一部分。它主要关注如何监控子进程的退出状态，并提供与子进程交互的异步 API。

**主要组成部分：**

1.  **`orphan` 模块和 `OrphanQueue`**:  用于处理“孤儿”进程，即父进程退出后，子进程仍然在运行的情况。`OrphanQueue` 负责跟踪这些孤儿进程，并在适当的时候清理它们。
2.  **`reap` 模块和 `Reaper`**:  `Reaper` 结构体用于处理子进程的退出信号 (SIGCHLD)。它使用 `tokio-net` 库中的 `Signal` 类型来监听 SIGCHLD 信号，并在收到信号时尝试获取子进程的退出状态。
3.  **`pidfd_reaper` 模块 (仅在 Linux 上启用)**:  如果启用了 `rt` 特性并且在 Linux 系统上，则使用 `pidfd_reaper` 模块。该模块使用 `pidfd` 机制来更有效地监控子进程的退出，避免了信号处理的复杂性。
4.  **`Child` 枚举**:  `Child` 是一个枚举，它封装了两种子进程监控方式：`SignalReaper` (基于信号) 和 `PidfdReaper` (基于 pidfd)。它实现了 `Future` trait，允许异步地等待子进程的退出。
5.  **`spawn_child` 函数**:  这个函数用于创建子进程。它使用 `std::process::Command` 来启动子进程，并根据系统和特性选择使用 `PidfdReaper` 或 `SignalReaper` 来监控子进程。它还处理子进程的 stdin、stdout 和 stderr。
6.  **`Pipe` 结构体**:  `Pipe` 结构体封装了文件描述符 (File)，用于表示子进程的 stdin、stdout 和 stderr。它实现了 `AsRawFd`、`AsFd`、`Read` 和 `Write` trait，使得 `Pipe` 可以被用于异步 I/O 操作。
7.  **`ChildStdio` 结构体**:  `ChildStdio` 结构体封装了 `Pipe`，并使用 `PollEvented` 来实现异步 I/O。它实现了 `AsyncRead` 和 `AsyncWrite` trait，允许异步地读取和写入子进程的 stdin、stdout 和 stderr。
8.  **`GlobalOrphanQueue` 结构体**:  实现了 `OrphanQueue` trait，用于管理孤儿进程。
9.  **`get_orphan_queue` 函数**:  获取全局的孤儿进程队列。
10. **`convert_to_stdio` 和 `stdio` 函数**:  用于将 `ChildStdio` 转换为 `Stdio`，并设置文件描述符为非阻塞模式。

**工作原理：**

*   当使用 `spawn_child` 启动一个子进程时，会根据系统和特性选择合适的监控方式。
*   如果使用 `SignalReaper`，则会创建一个 `Signal` 来监听 SIGCHLD 信号。当收到信号时，`Reaper` 会尝试获取子进程的退出状态。
*   如果使用 `PidfdReaper`，则会使用 `pidfd` 机制来监控子进程的退出。
*   `Child` 枚举实现了 `Future` trait，允许异步地等待子进程的退出。当 `Child` 被 `poll` 时，它会检查子进程的退出状态，并返回结果。
*   `ChildStdio` 结构体用于处理子进程的 stdin、stdout 和 stderr，并提供了异步 I/O 的能力。

**与其他部分的关联：**

*   与 `tokio` 库的 `runtime` 模块交互，使用 `Signal` 来处理信号。
*   与 `tokio` 库的 `io` 模块交互，使用 `AsyncRead` 和 `AsyncWrite` trait 来处理异步 I/O。
*   与 `tokio` 库的 `process::kill` 模块交互，实现 `Kill` trait。
*   与 `tokio` 库的 `process::SpawnedChild` 结构体交互，用于返回已生成的子进程。
