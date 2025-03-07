这个文件定义了 `WorkerMetrics` 结构体，用于收集和存储 Tokio 运行时中工作线程的各种性能指标。这些指标可以帮助开发者了解工作线程的行为，例如任务的执行情况、线程的空闲时间、任务窃取等，从而进行性能分析和优化。

**关键组件：**

*   `WorkerMetrics` 结构体：
    *   包含了多个 `MetricAtomicU64` 和 `MetricAtomicUsize` 类型的字段，用于原子地存储各种计数器和时间统计数据。这些字段涵盖了工作线程的多个方面，例如：
        *   `park_count`：工作线程停泊的次数。
        *   `park_unpark_count`：工作线程停泊和唤醒的次数。
        *   `noop_count`：工作线程在没有执行任务的情况下被唤醒并再次停泊的次数。
        *   `steal_count`：工作线程窃取任务的次数。
        *   `steal_operations`：工作线程窃取操作的次数。
        *   `poll_count`：工作线程轮询任务的次数。
        *   `mean_poll_time`：任务轮询时间的指数加权移动平均值（以纳秒为单位）。
        *   `busy_duration_total`：工作线程用于执行任务的时间总量。
        *   `local_schedule_count`：在工作线程的本地队列中调度的任务数量。
        *   `overflow_count`：将任务从本地队列移动到全局队列的次数。
        *   `queue_depth`：本地队列中当前的任务数量。
        *   `poll_count_histogram`：可选的直方图，用于跟踪轮询时间的分布。
        *   `thread_id`：工作线程的线程 ID。
    *   `from_config` 方法：根据给定的 `Config` 对象创建 `WorkerMetrics` 实例，并根据配置初始化 `poll_count_histogram`。
    *   `new` 方法：创建一个默认的 `WorkerMetrics` 实例。
    *   `queue_depth` 方法：获取本地队列的深度。
    *   `set_queue_depth` 方法：设置本地队列的深度。
    *   `thread_id` 方法：获取工作线程的线程 ID。
    *   `set_thread_id` 方法：设置工作线程的线程 ID。

**与其他组件的交互：**

*   `Config`：用于配置 `poll_count_histogram`。
*   `Histogram`：用于存储轮询时间的直方图数据。
*   `MetricAtomicU64` 和 `MetricAtomicUsize`：用于原子地更新性能指标。
*   `ThreadId`：用于标识工作线程。
