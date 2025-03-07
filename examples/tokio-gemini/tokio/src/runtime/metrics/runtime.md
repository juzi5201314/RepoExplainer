这个文件定义了 `RuntimeMetrics` 结构体，它提供了一个用于访问 Tokio 运行时各种指标的句柄。这些指标包括运行时使用的 worker 线程数量、存活任务数量、全局队列深度，以及在 `cfg_unstable_metrics!` 特性启用时，更多关于阻塞线程、线程 ID、任务计数、调度统计信息和 I/O 驱动程序指标的信息。

关键组件：

*   `RuntimeMetrics` 结构体：这是一个句柄，用于访问运行时的指标。它包含一个 `Handle` 字段，该字段指向运行时的内部结构。
*   `new` 函数：创建一个新的 `RuntimeMetrics` 实例。
*   各种 `num_*` 和 `*count` 函数：这些函数提供了访问各种运行时指标的方法，例如 `num_workers`、`num_alive_tasks`、`global_queue_depth` 等。这些函数通过访问 `Handle` 内部的结构来获取指标值。
*   `cfg_unstable_metrics!` 宏：这个宏用于条件编译，只有在启用 `unstable_metrics` 特性时，才会编译和提供一些更高级的指标，例如阻塞线程的数量、线程 ID、任务计数、调度统计信息和 I/O 驱动程序指标。
*   `cfg_64bit_metrics!` 宏：这个宏用于条件编译，只有在启用 `64bit_metrics` 特性时，才会编译和提供一些使用 64 位整数的指标，例如任务计数和调度统计信息。
*   `worker_thread_id` 函数：返回给定 worker 线程的 ID。
*   `poll_time_histogram_*` 函数：这些函数提供了访问任务轮询时间直方图相关指标的方法，只有在启用 `enable_metrics_poll_time_histogram()` 时才可用。
