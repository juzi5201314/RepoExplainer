这个文件定义了 `Handle` 结构体的一些方法，这些方法用于获取多线程调度器的各种度量指标。这些指标主要用于监控和调试 Tokio 运行时。

**关键组件:**

*   `Handle`:  代表多线程调度器的句柄，用于与调度器交互。
*   `cfg_unstable_metrics!`:  这是一个条件编译宏，只有在启用 `unstable-metrics` 特性时，才会包含相关的代码。这表明这些度量指标是实验性的，可能不稳定。
*   `num_workers()`:  返回调度器中工作线程的数量。
*   `num_alive_tasks()`:  返回当前存活的任务数量。
*   `injection_queue_depth()`:  返回注入队列的深度，注入队列用于将任务提交给调度器。
*   `spawned_tasks_count()`:  (仅在启用 `cfg_64bit_metrics` 时) 返回已生成的任务总数。
*   `num_blocking_threads()`:  返回阻塞线程的数量。阻塞线程用于执行阻塞操作，例如文件 I/O。
*   `num_idle_blocking_threads()`:  返回空闲的阻塞线程数量。
*   `scheduler_metrics()`:  返回调度器的度量指标，例如任务的平均执行时间等。
*   `worker_metrics()`:  返回指定工作线程的度量指标。
*   `worker_local_queue_depth()`:  返回指定工作线程的本地队列深度。
*   `blocking_queue_depth()`:  返回阻塞队列的深度。

**功能:**

这些方法提供了对 Tokio 运行时内部状态的访问，允许用户监控调度器的性能、任务的执行情况以及阻塞线程的使用情况。这些信息对于性能调优、故障排除和理解应用程序的行为至关重要。

**与项目的关系:**

这个文件是 Tokio 运行时的一部分，它提供了访问运行时内部度量指标的接口。这些指标可以帮助开发者了解 Tokio 运行时的工作方式，并优化他们的应用程序。
