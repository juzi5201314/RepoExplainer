这个文件定义了用于处理阻塞操作的线程池。它包含 `BlockingPool`、`Spawner` 和相关的结构体，用于在 Tokio 运行时中管理和调度阻塞任务。

**主要组件：**

*   **`BlockingPool`**:
    *   是阻塞操作线程池的主要结构体。
    *   包含一个 `Spawner` 用于生成任务，以及一个 `shutdown_rx` 用于接收关闭信号。
    *   `new` 函数用于创建 `BlockingPool`，并初始化线程池的配置，如线程数量限制、线程名称、堆栈大小等。
    *   `spawner` 方法返回一个 `Spawner` 实例，用于提交任务。
    *   `shutdown` 方法用于关闭线程池，等待所有任务完成或超时。
    *   `Drop` trait 的实现确保在 `BlockingPool` 实例被丢弃时，线程池会被关闭。
*   **`Spawner`**:
    *   用于向阻塞线程池提交任务。
    *   包含一个 `Inner` 结构体的 `Arc` 引用，用于共享线程池的状态。
    *   `spawn_blocking` 方法用于提交非强制性阻塞任务。
    *   `spawn_mandatory_blocking` 方法用于提交强制性阻塞任务（如果启用了 `fs` 特性）。
    *   `spawn_blocking_inner` 方法是 `spawn_blocking` 和 `spawn_mandatory_blocking` 的内部实现，它创建 `BlockingTask` 并将其提交到线程池。
    *   `spawn_task` 方法将任务添加到共享队列中，并根据需要启动新的工作线程。
    *   `spawn_thread` 方法用于创建新的工作线程。
*   **`Inner`**:
    *   包含线程池的共享状态，包括任务队列、通知计数器、关闭标志、线程名称、堆栈大小、回调函数、线程数量限制、保持活动时间以及度量指标。
    *   `run` 方法是工作线程的入口点，它从任务队列中获取任务并执行它们，并在空闲时等待新的任务。
*   **`Shared`**:
    *   包含在 `Inner` 结构体中，用于在线程之间共享状态。
    *   包含任务队列 (`queue`)、通知计数器 (`num_notify`)、关闭标志 (`shutdown`)、关闭发送者 (`shutdown_tx`)、最后一个退出线程的 `JoinHandle` (`last_exiting_thread`)、工作线程的 `JoinHandle` 集合 (`worker_threads`) 和工作线程索引 (`worker_thread_index`)。
*   **`Task`**:
    *   表示要执行的阻塞任务。
    *   包含一个 `task::UnownedTask` 和一个 `Mandatory` 标志，用于指示任务是否为强制性任务。
    *   `new` 方法用于创建 `Task` 实例。
    *   `run` 方法执行任务。
    *   `shutdown_or_run_if_mandatory` 方法根据任务的强制性标志来执行任务或关闭任务。
*   **`Mandatory`**:
    *   一个枚举，用于指示任务是否为强制性任务。
*   **`SpawnError`**:
    *   一个枚举，表示在生成任务时可能发生的错误，例如线程池关闭或无法创建新的工作线程。
*   **`SpawnerMetrics`**:
    *   用于收集线程池的度量指标，例如线程数量、空闲线程数量和队列深度。

**工作流程：**

1.  当需要执行阻塞操作时，使用 `spawn_blocking` 或 `spawn_mandatory_blocking` 函数。
2.  这些函数通过 `Spawner` 将任务提交到阻塞线程池。
3.  `Spawner` 将任务添加到共享的任务队列中。
4.  如果当前没有空闲的工作线程，`Spawner` 可能会启动新的工作线程。
5.  工作线程从任务队列中获取任务并执行它们。
6.  工作线程在空闲时等待新的任务，并使用条件变量进行同步。
7.  当线程池关闭时，所有工作线程都会被通知并退出。

**与其他组件的交互：**

*   与 Tokio 运行时交互：`BlockingPool` 和 `Spawner` 是 Tokio 运行时的一部分，用于处理阻塞操作。
*   与任务调度器交互：`BlockingTask` 用于将阻塞操作包装成 Tokio 运行时可以调度的任务。
*   与 `shutdown` 模块交互：`BlockingPool` 使用 `shutdown` 模块来处理线程池的关闭。
*   与 `loom` 模块交互：在测试和某些情况下，使用 `loom` 模块进行并发测试。
