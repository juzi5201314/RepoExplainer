这段代码文件定义了 `Stats` 结构体，用于收集和管理多线程 Tokio 运行时调度器的统计信息。它主要用于调整调度器行为和报告运行时级别的指标。

**关键组件：**

*   **`Stats` 结构体：**
    *   `batch`:  `MetricsBatch` 类型的实例，用于向用户报告运行时级别的指标和统计数据。
    *   `task_poll_time_ewma`:  一个指数加权移动平均值 (EWMA)，用于跟踪轮询已调度任务所花费的时间。使用 `f64` 类型存储，以方便 EWMA 计算。

*   **`Ephemeral` 结构体：**
    *   `processing_scheduled_tasks_started_at`:  记录上次恢复工作（从 park 状态继续）的时刻。
    *   `tasks_polled_in_batch`:  记录在批处理的已调度任务中轮询的任务数量。
    *   `batch_started`:  仅在调试模式下使用，用于确保 `start_processing_scheduled_tasks` 和 `end_processing_scheduled_tasks` 的调用是配对的。

*   **常量：**
    *   `TASK_POLL_TIME_EWMA_ALPHA`:  EWMA 计算中使用的 alpha 值，用于确定每个单独轮询时间的权重。
    *   `TARGET_GLOBAL_QUEUE_INTERVAL`:  全局队列间隔的目标值（微秒）。
    *   `MAX_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`:  全局队列间隔的最大值。
    *   `TARGET_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`:  全局队列间隔的目标任务数。
    *   `DEFAULT_GLOBAL_QUEUE_INTERVAL`:  全局队列间隔的默认值。

*   **方法：**
    *   `new()`:  创建 `Stats` 实例，并使用期望值初始化 `task_poll_time_ewma`。
    *   `tuned_global_queue_interval()`:  根据配置和 `task_poll_time_ewma` 值，计算并返回调整后的全局队列间隔。如果配置中显式设置了间隔，则直接返回该值。
    *   `submit()`:  将统计数据提交到 `WorkerMetrics`。
    *   `about_to_park()`:  通知 `MetricsBatch` 即将进入 park 状态。
    *   `unparked()`:  通知 `MetricsBatch` 已经从 park 状态恢复。
    *   `inc_local_schedule_count()`:  增加本地调度计数。
    *   `start_processing_scheduled_tasks()`:  开始处理已调度的任务，初始化 `Ephemeral` 状态。
    *   `end_processing_scheduled_tasks()`:  结束处理已调度的任务，并根据轮询时间和任务数量更新 `task_poll_time_ewma`。
    *   `start_poll()`:  开始轮询任务，增加 `tasks_polled_in_batch`。
    *   `end_poll()`:  结束轮询任务。
    *   `incr_steal_count()`:  增加窃取计数。
    *   `incr_steal_operations()`:  增加窃取操作计数。
    *   `incr_overflow_count()`:  增加溢出计数。

**功能：**

该文件定义了用于收集和管理 Tokio 运行时调度器统计信息的结构体和方法。它跟踪任务轮询时间，并使用这些信息来调整全局队列间隔，从而优化调度器的性能。它还提供了用于报告各种运行时指标的接口。

**与其他组件的交互：**

*   与 `MetricsBatch` 交互，用于报告运行时指标。
*   与 `Config` 交互，用于获取配置信息，例如全局队列间隔。
*   与 `WorkerMetrics` 交互，用于提交统计数据。
