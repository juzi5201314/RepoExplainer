该文件定义了 `Handle` 结构体的一系列方法，这些方法用于获取 Tokio 运行时调度器的各种度量指标。这些指标提供了关于运行时状态的详细信息，例如工作线程的数量、阻塞线程的数量、任务数量、队列深度等。

**关键组件：**

*   **`Handle` 结构体：**  该结构体代表了 Tokio 运行时调度器的句柄，用于与运行时交互。
*   **`SchedulerMetrics` 和 `WorkerMetrics`：**  这两个结构体分别用于存储调度器和工作线程的度量指标。
*   **`blocking_spawner`：**  用于管理阻塞操作的线程池。
*   **各种方法：**  这些方法提供了对运行时指标的访问，包括：
    *   `num_workers()`:  获取工作线程的数量。
    *   `num_blocking_threads()`:  获取阻塞线程的数量。
    *   `num_idle_blocking_threads()`:  获取空闲阻塞线程的数量。
    *   `num_alive_tasks()`:  获取当前存活的任务数量。
    *   `spawned_tasks_count()`:  获取已创建的任务总数 (仅在 64 位指标配置下)。
    *   `scheduler_metrics()`:  获取调度器的度量指标。
    *   `worker_metrics(worker: usize)`:  获取指定工作线程的度量指标。
    *   `injection_queue_depth()`:  获取注入队列的深度。
    *   `worker_local_queue_depth(worker: usize)`:  获取指定工作线程的本地队列深度。
    *   `blocking_queue_depth()`:  获取阻塞队列的深度。

**功能：**

该文件中的代码提供了获取 Tokio 运行时内部状态的接口。这些指标对于监控、调试和性能分析至关重要。通过这些方法，可以了解运行时的工作负载、线程利用率、任务状态等信息。

**与项目的关系：**

该文件是 Tokio 运行时调度器的一部分，它提供了获取运行时内部状态的接口。这些接口被用于监控和调试 Tokio 运行时。
