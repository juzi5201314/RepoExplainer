这个文件 `idle.rs` 实现了 Tokio 运行时多线程调度器中用于协调空闲工作线程的逻辑。它定义了 `Idle` 和 `Synced` 两个结构体，以及与它们交互的各种方法，用于跟踪和管理工作线程的状态，包括搜索任务、休眠和唤醒。

**关键组件：**

*   **`Idle` 结构体：**
    *   `state: AtomicUsize`：原子整数，用于跟踪正在搜索任务的工作线程数量和已唤醒的工作线程数量。使用位运算进行优化，避免了不必要的锁竞争。
    *   `num_workers: usize`：总的工作线程数量。
*   **`Synced` 结构体：**
    *   `sleepers: Vec<usize>`：一个向量，存储了当前处于休眠状态的工作线程的索引。这个结构体的数据由调度器互斥锁保护。
*   **`State` 结构体：**
    *   一个内部结构体，用于封装和操作 `state` 原子整数的值，提供了方便的方法来获取和修改搜索线程和已唤醒线程的数量。
*   **常量：**
    *   `UNPARK_SHIFT`、`UNPARK_MASK`、`SEARCH_MASK`：用于位运算的常量，用于从 `state` 原子整数中提取和设置状态信息。
*   **方法：**
    *   `new(num_workers: usize) -> (Idle, Synced)`：创建一个新的 `Idle` 实例和 `Synced` 实例。
    *   `worker_to_notify(&self, shared: &Shared) -> Option<usize>`：如果当前没有工作线程正在搜索任务，则返回一个休眠的工作线程的索引，以便唤醒它。
    *   `transition_worker_to_parked(&self, shared: &Shared, worker: usize, is_searching: bool) -> bool`：将一个工作线程转移到休眠状态。
    *   `transition_worker_to_searching(&self) -> bool`：将一个工作线程转移到搜索任务状态。
    *   `transition_worker_from_searching(&self) -> bool`：将一个工作线程从搜索任务状态转移到运行状态。
    *   `unpark_worker_by_id(&self, shared: &Shared, worker_id: usize) -> bool`：根据工作线程 ID 唤醒一个特定的工作线程。
    *   `is_parked(&self, shared: &Shared, worker_id: usize) -> bool`：检查一个工作线程是否处于休眠状态。
    *   `notify_should_wakeup(&self) -> bool`：判断是否应该唤醒一个工作线程。
    *   `State` 结构体的方法：`new`、`load`、`unpark_one`、`inc_num_searching`、`dec_num_searching`、`dec_num_unparked`、`num_searching`、`num_unparked`：用于操作和访问 `state` 原子整数中的状态信息。

**工作流程：**

1.  **线程状态转换：** 工作线程可以在搜索任务、运行任务和休眠状态之间转换。
2.  **搜索任务：** 当没有任务可运行时，工作线程会进入搜索任务状态，尝试从任务队列中获取任务。
3.  **休眠：** 当没有任务可搜索时，工作线程会进入休眠状态，等待被唤醒。
4.  **唤醒：** 当有新的任务提交时，或者其他工作线程完成任务后，调度器会唤醒一个或多个休眠的工作线程。
5.  **状态同步：** 使用原子操作和互斥锁来确保线程状态的正确同步，避免数据竞争。

**与其他组件的交互：**

*   `Shared`：`Idle` 结构体通过 `Shared` 结构体访问共享数据，例如 `Synced` 结构体，`Shared` 结构体通常包含调度器相关的共享状态。
*   `worker`：`Idle` 结构体与工作线程交互，管理它们的状态。
*   `loom`：使用 `loom` 库进行并发测试，确保代码的正确性。
