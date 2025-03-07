这个文件定义了 `SchedulerMetrics` 结构体，用于收集 Tokio 运行时调度器的指标。

**主要组成部分：**

*   **`SchedulerMetrics` 结构体：**
    *   `remote_schedule_count`:  一个 `MetricAtomicU64` 类型的原子变量，用于记录从运行时外部调度的任务数量。
    *   `budget_forced_yield_count`:  一个 `MetricAtomicU64` 类型的原子变量，用于记录由于预算耗尽而强制让出的任务数量。
*   **`new()` 方法：**  创建一个新的 `SchedulerMetrics` 实例，并将两个计数器的初始值设置为 0。
*   **`inc_remote_schedule_count()` 方法：**  增加 `remote_schedule_count` 的值，表示从运行时外部调度了一个任务。
*   **`inc_budget_forced_yield_count()` 方法：** 增加 `budget_forced_yield_count` 的值，表示一个任务由于预算耗尽而被迫让出。

**功能和作用：**

`SchedulerMetrics` 结构体及其相关方法提供了对 Tokio 运行时调度器行为的度量。这些指标可以用于监控、调试和性能分析。例如，`remote_schedule_count` 可以帮助了解外部任务对运行时调度的影响，而 `budget_forced_yield_count` 可以指示任务是否频繁耗尽预算，从而影响性能。这些指标可以帮助开发者优化 Tokio 运行时和应用程序的性能。
