这个文件定义了 `Idle` 结构体，用于协调多线程 Tokio 运行时中的空闲工作线程。它负责跟踪空闲核心的数量，管理空闲核心的映射，并处理工作线程的休眠和唤醒。

**关键组件：**

*   `Idle`：核心结构体，包含以下字段：
    *   `num_searching`：原子计数器，表示正在搜索任务的核心数量。
    *   `num_idle`：原子计数器，表示空闲核心的数量。
    *   `idle_map`：`IdleMap` 结构体，用于跟踪哪些核心是空闲的。
    *   `needs_searching`：原子布尔值，用于指示是否需要搜索空闲工作线程。
    *   `num_cores`：总核心数量。
*   `IdleMap`：用于跟踪哪些核心是空闲的。它使用一个 `Vec<AtomicUsize>` 来存储核心的空闲状态，每个 `AtomicUsize` 代表一组核心。
*   `Snapshot`：用于创建 `IdleMap` 的快照，以便在不持有锁的情况下检查核心的空闲状态。
*   `Synced`：包含由调度器互斥锁同步的数据，包括：
    *   `sleepers`：一个 `Vec<usize>`，存储当前休眠的工作线程的 ID。
    *   `available_cores`：一个 `Vec<Box<Core>>`，存储可用的核心。
*   `Core`：表示一个核心。
*   `Handle`：用于管理运行时。
*   `Shared`：包含在线程之间共享的数据。

**功能：**

*   `new`：创建一个新的 `Idle` 实例和对应的 `Synced` 实例。
*   `needs_searching`：检查是否需要搜索空闲工作线程。
*   `num_idle`：获取空闲核心的数量。
*   `num_searching`：获取正在搜索任务的核心数量。
*   `snapshot`：创建 `IdleMap` 的快照。
*   `try_acquire_available_core`：尝试获取一个可用的核心。
*   `notify_local`：通知本地工作线程。
*   `notify_remote`：通知远程工作线程。
*   `notify_synced`：在同步状态下通知工作线程。
*   `notify_mult`：通知多个工作线程。
*   `shutdown`：关闭运行时。
*   `shutdown_unassigned_cores`：关闭未分配的核心。
*   `release_core`：释放核心，使其可供其他工作线程使用。
*   `transition_worker_to_parked`：将工作线程转换为休眠状态。
*   `try_transition_worker_to_searching`：尝试将工作线程转换为搜索状态。
*   `transition_worker_to_searching_if_needed`：如果需要，将工作线程转换为搜索状态。
*   `transition_worker_to_searching`：将工作线程转换为搜索状态。
*   `transition_worker_from_searching`：将工作线程从搜索状态转换。

**与其他组件的交互：**

*   `Idle` 与 `worker` 模块交互，管理工作线程的休眠和唤醒。
*   `Idle` 使用 `Shared` 结构体来访问共享数据，例如条件变量。
*   `Idle` 使用 `Handle` 来管理运行时。
*   `Idle` 使用 `Core` 来表示核心。
