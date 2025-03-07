这个文件定义了用于 Tokio 运行时跟踪的宏。它主要用于在异步操作的轮询过程中记录信息，以便进行调试和性能分析。

**关键组件：**

*   `cfg_trace!`：这是一个条件编译宏，只有在启用了跟踪功能时才会包含其内部定义。
*   `trace_op!` 宏：
    *   接收一个操作名称 `$name` 和一个布尔值 `$readiness` (表示操作是否已就绪)。
    *   使用 `tracing::trace!` 宏记录一条跟踪消息。
    *   消息的目标是 `"runtime::resource::poll_op"`。
    *   消息包含操作名称 `op_name` 和就绪状态 `is_ready`。
*   `trace_poll_op!` 宏：
    *   接收一个操作名称 `$name` 和一个 `Poll` 枚举 `$poll`。
    *   使用 `match` 语句检查 `$poll` 的状态。
    *   如果 `$poll` 是 `Poll::Ready`，则调用 `trace_op!` 宏，并将就绪状态设置为 `true`，然后返回 `Poll::Ready`。
    *   如果 `$poll` 是 `Poll::Pending`，则调用 `trace_op!` 宏，并将就绪状态设置为 `false`，然后返回 `Poll::Pending`。

**功能：**

这些宏的主要目的是在异步操作的轮询过程中记录信息。通过使用 `trace_op!` 和 `trace_poll_op!`，可以跟踪每个操作的轮询状态（是否已就绪），这对于理解 Tokio 运行时内部的异步操作流程、诊断性能问题和调试并发问题非常有帮助。

**与项目的关系：**
