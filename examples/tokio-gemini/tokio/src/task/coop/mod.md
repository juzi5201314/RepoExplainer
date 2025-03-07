这个文件 `mod.rs` 位于 `tokio/src/task/coop/` 目录下，实现了 Tokio 的协作式调度机制。其主要目的是防止长时间运行的任务独占执行器，从而导致其他任务饿死。

**主要组成部分：**

1.  **`Budget` 结构体：**
    *   表示任务在让出执行权之前可以执行的“工作量”。
    *   `initial()` 方法返回一个初始预算值。
    *   `unconstrained()` 方法返回一个无限制预算，即任务不受协作式调度限制。
    *   `has_remaining()` 方法检查预算是否还有剩余。

2.  **`budget` 和 `with_unconstrained` 函数：**
    *   `budget` 函数：在给定的闭包中设置一个协作式调度预算。闭包执行完毕后，预算会被重置。
    *   `with_unconstrained` 函数：在给定的闭包中设置一个无限制的预算，即禁用协作式调度。

3.  **`has_budget_remaining` 函数：**
    *   检查当前任务是否还有剩余预算。

4.  **`poll_proceed` 函数（仅在 `cfg_coop` 特性启用时）：**
    *   在轮询一个 future 之前调用，用于检查任务是否超出了预算。
    *   如果预算已耗尽，则返回 `Poll::Pending`，迫使任务让出执行权。
    *   返回一个 `RestoreOnPending` 结构体，用于在任务完成或被取消时恢复预算。

5.  **`Coop` 结构体（仅在 `cfg_coop` 特性启用时）：**
    *   一个 future 包装器，用于确保协作式调度。
    *   在 `poll` 方法中，在轮询内部 future 之前调用 `poll_proceed`。
    *   如果内部 future 完成，则调用 `RestoreOnPending::made_progress`。

6.  **`cooperative` 函数（仅在 `cfg_coop` 特性启用时）：**
    *   创建一个 `Coop` 结构体，用于包装给定的 future，从而启用协作式调度。

7.  **`RestoreOnPending` 结构体（仅在 `cfg_coop` 特性启用时）：**
    *   用于在 `poll_proceed` 返回 `Poll::Pending` 时，保存当前预算，并在 future 再次被轮询时恢复。
    *   `made_progress` 方法用于指示任务取得了进展，从而避免在任务完成时恢复预算。

8.  **`consume_budget` 和 `unconstrained` 模块：**
    *   这两个模块分别提供了消耗预算和取消预算限制的功能。

**工作原理：**

*   Tokio 的协作式调度通过给每个任务分配一个预算来实现。
*   在任务的 `poll` 方法中，会周期性地调用 `poll_proceed` 来检查预算。
*   如果预算耗尽，`poll_proceed` 返回 `Poll::Pending`，任务必须让出执行权。
*   当任务再次被轮询时，会重新获得预算。
*   `unconstrained` 函数允许开发者绕过协作式调度，例如对于需要长时间运行且不应该被中断的任务。

**与其他部分的关联：**

*   与 Tokio 的运行时（`rt` 特性）紧密结合，提供了协作式调度的核心功能。
*   `task::unconstrained` 函数允许开发者绕过协作式调度。
*   `tokio::time` 模块中的 `Sleep` 结构体使用协作式调度来避免长时间阻塞。
