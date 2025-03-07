这个文件定义了 Tokio 运行时多线程调度器中的工作线程 (`Worker`) 及其核心数据结构 (`Core`)。它负责管理任务的执行、调度和运行时关闭流程。

**主要组成部分：**

*   **`Worker` 结构体：**
    *   代表一个工作线程，包含线程本地状态，如 `tick`（用于调度簿记任务）、`is_shutdown`（指示是否正在关闭）、`is_traced`（指示是否正在跟踪）、`num_seq_local_queue_polls`（用于控制从本地队列或注入队列轮询的频率）、`global_queue_interval`（全局队列轮询间隔）、`workers_to_notify`（需要通知的工作线程列表）、`idle_snapshot`（空闲核心列表的快照）和 `stats`（统计信息）。
*   **`Core` 结构体：**
    *   代表工作线程的核心数据，存储在堆上，可以在线程之间迁移。包含：
        *   `index`：核心的索引。
        *   `lifo_slot`：一个可选的 `Notified` 任务，用于 LIFO（后进先出）调度。
        *   `run_queue`：工作线程的本地运行队列。
        *   `is_searching`：指示工作线程是否正在寻找更多工作（尝试从其他线程窃取任务）。
        *   `stats`：每个工作线程的运行时统计信息。
        *   `rand`：快速随机数生成器。
*   **`Shared` 结构体：**
    *   存储所有工作线程共享的状态。包含：
        *   `remotes`：`Remote` 结构的数组，用于与其他工作线程通信。
        *   `inject`：全局任务队列，用于在非工作线程或工作线程的本地队列饱和时提交任务。
        *   `idle`：用于协调空闲工作线程。
        *   `owned`：所有已生成任务的集合。
        *   `synced`：由调度器互斥锁同步的数据。
        *   `driver`：Tokio 的 I/O、定时器等的驱动程序。
        *   `condvars`：用于唤醒工作线程的条件变量。
        *   `trace_status`：跟踪信号的状态。
        *   `config`：调度器配置选项。
        *   `scheduler_metrics`：从运行时收集的指标。
        *   `worker_metrics`：每个工作线程的指标。
        *   `_counters`：用于收集内部运行时指标的计数器（仅在启用 `tokio_internal_mt_counters` 特性时）。
*   **`Synced` 结构体：**
    *   由调度器互斥锁保护的数据。包含：
        *   `assigned_cores`：已分配核心的向量。
        *   `shutdown_cores`：观察到关闭信号的核心。
        *   `shutdown_driver`：关闭期间的驱动程序。
        *   `idle`：`Idle` 的同步状态。
        *   `inject`：`Inject` 的同步状态。
*   **`Remote` 结构体：**
    *   用于从其他线程与工作线程通信。包含：
        *   `steal`：从该工作线程窃取任务的队列。
*   **`Context` 结构体：**
    *   线程本地上下文，包含：
        *   `handle`：当前调度器的句柄。
        *   `index`：工作线程的索引。
        *   `lifo_enabled`：LIFO 槽是否启用。
        *   `core`：核心数据。
        *   `handoff_core`：当调用 `block_in_place` 时，用于将核心传递给其他线程。
        *   `defer`：在轮询资源驱动程序后要唤醒的任务。
*   **`RunResult`、`NextTaskResult`、`Task`、`Notified`：**
    *   类型别名，用于简化代码。
*   **常量：**
    *   `MAX_LIFO_POLLS_PER_TICK`：LIFO 槽在一次 tick 中轮询的最大次数。

**功能和流程：**

1.  **初始化：** `create` 函数创建多线程调度器，初始化工作线程、核心、共享状态和驱动程序。
2.  **`block_in_place`：** 当在工作线程中调用 `block_in_place` 时，将当前工作线程的核心数据移动到另一个线程，以便调度器可以继续运行。
3.  **`run` 函数：** 工作线程的主循环，负责：
    *   从本地队列、LIFO 槽或注入队列中获取任务。
    *   运行任务。
    *   如果本地队列为空，则尝试从其他工作线程窃取任务。
    *   定期执行维护任务。
    *   处理关闭信号。
4.  **任务调度：**
    *   `schedule_task`：将任务添加到本地队列或注入队列。
    *   `schedule_remote`：将任务添加到注入队列，并通知工作线程。
    *   `next_task`：查找要运行的下一个任务，优先从 LIFO 槽、本地队列和注入队列中获取。
5.  **任务窃取：** `search_for_work` 函数尝试从其他工作线程窃取任务。
6.  **关闭流程：**
    *   `Shared::close`：关闭注入队列和 `OwnedTasks` 实例，并唤醒所有工作线程。
    *   工作线程检测到关闭信号，并执行清理操作。
    *   工作线程调用 `Shared::shutdown` 进入单线程关闭阶段。
    *   清空本地运行队列和注入队列。

**与其他文件的关系：**

*   与 `crate::runtime` 模块交互，获取配置信息、驱动程序和任务句柄。
*   使用 `crate::loom` 模块中的同步原语。
*   使用 `crate::runtime::scheduler` 模块中的调度器相关结构。
*   使用 `crate::runtime::task` 模块中的任务相关结构。
*   使用 `crate::runtime::driver` 模块中的驱动程序。
*   使用 `crate::runtime::blocking` 模块中的阻塞操作。
*   使用 `crate::task::coop` 模块中的协作调度。
*   使用 `crate::util::atomic_cell` 模块中的原子单元。
*   使用 `crate::util::rand` 模块中的随机数生成器。
