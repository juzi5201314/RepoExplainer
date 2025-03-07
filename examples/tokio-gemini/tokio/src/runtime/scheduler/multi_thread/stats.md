这个文件定义了 `Stats` 结构体，用于收集和管理多线程 Tokio 运行时调度器的统计信息。它主要用于调整调度器和报告运行时级别的指标/统计数据。

**关键组件：**

*   `Stats` 结构体：
    *   `batch`:  `MetricsBatch` 结构体，用于向用户报告运行时级别的指标/统计数据。
    *   `processing_scheduled_tasks_started_at`:  `Instant` 类型，记录上次恢复工作的时间（从 park 状态恢复）。
    *   `tasks_polled_in_batch`:  `usize` 类型，记录在当前批次中轮询的任务数量。
    *   `task_poll_time_ewma`:  `f64` 类型，指数加权移动平均值，用于衡量轮询一个任务所花费的时间。
*   常量：
    *   `TASK_POLL_TIME_EWMA_ALPHA`:  `f64` 类型，用于计算 EWMA 的权重。
    *   `TARGET_GLOBAL_QUEUE_INTERVAL`:  `f64` 类型，目标全局队列间隔（微秒）。
    *   `MAX_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`:  `u32` 类型，全局队列间隔的最大任务数。
    *   `TARGET_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`:  `u32` 类型，全局队列间隔的目标任务数。
*   `impl Stats` 块：
    *   `new()`：构造函数，初始化 `Stats` 结构体。
    *   `tuned_global_queue_interval()`：根据配置和统计信息，调整全局队列的间隔。
    *   `submit()`：提交统计数据。
    *   `about_to_park()`：通知即将进入 park 状态。
    *   `unparked()`：通知从 park 状态恢复。
    *   `inc_local_schedule_count()`：增加本地调度计数。
    *   `start_processing_scheduled_tasks()`：开始处理已调度的任务。
    *   `end_processing_scheduled_tasks()`：结束处理已调度的任务，并更新 EWMA 任务轮询时间。
    *   `start_poll()`：开始轮询任务。
    *   `end_poll()`：结束轮询任务。
    *   `incr_steal_count()`：增加窃取计数。
    *   `incr_steal_operations()`：增加窃取操作计数。
    *   `incr_overflow_count()`：增加溢出计数。

**功能：**

该文件主要负责收集和维护调度器的性能统计数据，并根据这些数据进行自适应调整。它跟踪任务轮询时间、全局队列间隔等关键指标，以便优化调度器的性能。

**与其他组件的交互：**

*   与 `MetricsBatch` 交互，用于报告运行时指标。
*   与 `Config` 交互，用于获取配置信息，例如全局队列间隔。
*   与 `WorkerMetrics` 交互，用于收集每个 worker 的统计信息。
