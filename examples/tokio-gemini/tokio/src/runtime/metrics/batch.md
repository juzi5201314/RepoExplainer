这个文件定义了 `MetricsBatch` 结构体，用于收集 Tokio 运行时中工作线程的性能指标。它主要用于批处理收集各种计数器和时间信息，然后将这些信息提交给 `WorkerMetrics`，以便进行全局监控和分析。

**关键组件：**

*   **`MetricsBatch` 结构体：**
    *   包含各种计数器，例如 `park_count`（工作线程停泊次数）、`poll_count`（任务轮询次数）、`steal_count`（任务窃取次数）等。
    *   `busy_duration_total` 记录了工作线程处理任务的总时间。
    *   `poll_timer` (可选) 用于测量任务轮询时间，使用 `HistogramBatch` 来存储轮询时间的分布。
    *   `processing_scheduled_tasks_started_at` 记录了开始处理一批任务的时间。
*   **`PollTimer` 结构体：**
    *   用于测量任务轮询时间。
    *   `poll_counts` 是一个 `HistogramBatch`，用于存储轮询时间的直方图数据。
    *   `poll_started_at` 记录了最近一次任务轮询开始的时间。
*   **`new()` 方法：**
    *   创建一个新的 `MetricsBatch` 实例，并初始化所有计数器。
    *   如果启用了轮询时间直方图，则初始化 `poll_timer`。
*   **`submit()` 方法：**
    *   将 `MetricsBatch` 中收集的指标提交给 `WorkerMetrics`，更新工作线程的全局指标。
    *   如果启用了轮询时间直方图，则提交直方图数据。
*   **`about_to_park()` 方法：**
    *   当工作线程即将停泊时调用，更新 `park_count` 和 `park_unpark_count`。
    *   如果工作线程在停泊前没有执行任何任务，则增加 `noop_count`。
*   **`unparked()` 方法：**
    *   当工作线程被唤醒时调用，更新 `park_unpark_count`。
*   **`start_processing_scheduled_tasks()` 和 `end_processing_scheduled_tasks()` 方法：**
    *   用于测量工作线程处理任务的总时间。
*   **`start_poll()` 和 `end_poll()` 方法：**
    *   用于测量单个任务的轮询时间。
*   **`inc_local_schedule_count()` 方法：**
    *   增加本地任务调度计数。
*   **`incr_steal_count()`、`incr_steal_operations()` 和 `incr_overflow_count()` 方法：**
    *   这些方法仅在多线程运行时配置下可用，用于更新任务窃取和溢出相关的计数器。
*   **`duration_as_u64()` 函数：**
    *   将 `Duration` 转换为 `u64` 类型的纳秒数，如果转换失败，则返回 `u64::MAX`。

**与其他组件的交互：**

*   `MetricsBatch` 收集工作线程的运行时指标。
*   `WorkerMetrics` 存储工作线程的全局指标，`MetricsBatch` 将收集到的指标提交给 `WorkerMetrics`。
*   `HistogramBatch` 用于批处理轮询时间的直方图数据。
*   `cfg_rt_multi_thread!` 宏用于根据运行时配置启用多线程相关的指标。
