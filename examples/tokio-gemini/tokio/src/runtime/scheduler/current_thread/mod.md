这个文件定义了 `tokio` 运行时中用于在当前线程上执行任务的调度器。它包含 `CurrentThread` 结构体，该结构体负责管理任务队列、驱动程序和线程本地上下文。

**关键组件：**

*   **`CurrentThread`**:  这是当前线程调度器的主要结构体。它包含一个 `AtomicCell` 类型的 `core` 字段，用于存储调度器的核心数据，以及一个 `Notify` 字段，用于唤醒其他线程来窃取驱动程序。
*   **`Handle`**:  这是当前线程调度器的句柄，用于在运行时中共享状态。它包含共享状态 (`Shared`)、驱动程序句柄 (`driver`)、阻塞池生成器 (`blocking_spawner`)、随机数生成器 (`seed_generator`)、任务钩子 (`task_hooks`) 和线程 ID (`local_tid`)。
*   **`Core`**:  包含调度器运行所需的核心数据，如任务队列 (`tasks`)、当前滴答数 (`tick`)、驱动程序 (`driver`)、度量批处理 (`metrics`)、全局队列间隔 (`global_queue_interval`) 和未处理的 panic 标志 (`unhandled_panic`)。
*   **`Shared`**:  包含在线程之间共享的调度器状态，如注入队列 (`inject`)、拥有的任务集合 (`owned`)、唤醒标志 (`woken`)、配置 (`config`)、调度器度量 (`scheduler_metrics`) 和工作线程度量 (`worker_metrics`)。
*   **`Context`**:  线程本地上下文，用于存储调度器句柄、核心数据和延迟任务。
*   **`Notified`**:  一个类型别名，表示已通知的任务。
*   **`CoreGuard`**:  一个辅助结构体，用于确保在 `block_on` 期间，即使 future 发生 panic，`Core` 值也会放回其槽位。

**功能：**

*   **`new`**:  创建一个新的 `CurrentThread` 调度器，初始化驱动程序、阻塞池、随机数生成器和配置。
*   **`block_on`**:  在当前线程上阻塞，直到给定的 future 完成。它尝试窃取调度器核心并执行 future，如果失败，则等待通知或 future 完成。
*   **`take_core`**:  尝试获取调度器核心。
*   **`shutdown`**:  关闭调度器，释放资源，并处理所有剩余的任务。
*   **`spawn` 和 `spawn_local`**:  将 future 提交到调度器以供执行。
*   **`dump`**:  （可选，如果启用了 `tokio_taskdump` 特性）捕获此运行时状态的快照。
*   **`next_remote_task`**:  从远程队列获取下一个任务。
*   **`reset_woken`**:  重置唤醒标志并返回原始值。
*   **`num_alive_tasks`**:  返回活动任务的数量。
*   **`injection_queue_depth`**:  返回注入队列的深度。

**与其他组件的交互：**

*   **`driver`**:  `CurrentThread` 调度器使用驱动程序来处理 I/O 事件、定时器事件等。
*   **`blocking`**:  调度器使用阻塞池来执行阻塞操作。
*   **`task`**:  调度器管理任务的生命周期，包括创建、调度和执行。
*   **`scheduler`**:  `CurrentThread` 实现了 `Schedule` trait，允许任务被调度到当前线程。
*   **`context`**:  调度器使用线程本地上下文来存储调度器状态。

**总结：**
