这个文件定义了 `Unconstrained` 结构体和 `unconstrained` 函数，它们用于在 Tokio 运行时中禁用协程调度。

**主要组成部分：**

*   **`Unconstrained<F>` 结构体:**
    *   这是一个 `Future` 的包装器，使用 `pin_project` 宏来确保 `inner` 字段可以被安全地固定。
    *   `inner` 字段： 存储被包装的 `Future`。
*   **`unconstrained<F>(inner: F) -> Unconstrained<F>` 函数:**
    *   这是一个公共函数，用于创建一个 `Unconstrained` 实例。
    *   它接受一个 `Future` 作为参数，并将其包装在 `Unconstrained` 结构体中。
*   **`impl Future for Unconstrained<F>`:**
    *   为 `Unconstrained` 结构体实现了 `Future` trait。
    *   `poll` 方法：
        *   根据编译时配置 (`cfg_coop!` 和 `cfg_not_coop!`)，决定如何轮询内部的 `Future`。
        *   如果启用了协程调度 (`cfg_coop!`)，则使用 `crate::task::coop::with_unconstrained` 函数来在无约束的环境中轮询内部的 `Future`。这意味着 Tokio 运行时不会强制该 `Future` 产生 yield。
        *   如果未启用协程调度 (`cfg_not_coop!`)，则直接轮询内部的 `Future`。

**功能和作用：**

*   `unconstrained` 函数允许开发者禁用对特定 `Future` 的协程调度。这使得该 `Future` 可以在不被 Tokio 运行时强制 yield 的情况下运行。
*   这对于需要长时间运行且不希望被中断的任务（例如，某些 I/O 操作或计算密集型任务）可能很有用。
*   **重要提示：** 使用 `unconstrained` 需要谨慎，因为如果被包装的 `Future` 永远不 yield，可能会导致其他任务饿死。

**与项目的关系：**

这个文件是 Tokio 运行时的一部分，它提供了控制任务调度行为的机制。它允许开发者在需要时禁用协程调度，从而优化特定任务的性能。
