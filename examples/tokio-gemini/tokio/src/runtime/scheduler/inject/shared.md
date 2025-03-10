这个文件定义了 `Shared` 结构体，它用于在 Tokio 运行时中实现任务注入队列的共享状态。它与 `Synced` 结构体协同工作，后者负责同步访问队列。

**关键组件：**

*   `Shared<T>`：
    *   `len: AtomicUsize`：原子整数，用于跟踪队列中待处理任务的数量。这有助于在热路径中避免不必要的锁定。
    *   `_p: PhantomData<T>`：一个 PhantomData，用于标记队列中存储的任务类型。
    *   `new()`：创建一个新的 `Shared` 实例和一个 `Synced` 实例。
    *   `is_empty()`：检查队列是否为空。
    *   `is_closed()`：检查注入队列是否已关闭（仅在特定配置下可用）。
    *   `close()`：关闭注入队列。
    *   `len()`：获取队列中任务的数量。
    *   `push()`：将任务推入队列。
    *   `pop()`：从队列中弹出一个任务。
    *   `pop_n()`：从队列中弹出 `n` 个任务。
*   `Synced`：
    *   `is_closed`：一个布尔值，指示队列是否已关闭。
    *   `head`：指向队列头部的指针。
    *   `tail`：指向队列尾部的指针。

**工作原理：**

`Shared` 结构体和 `Synced` 结构体共同构成了一个线程安全的任务注入队列。`Shared` 结构体包含一个原子计数器 `len`，用于跟踪队列中的任务数量，从而减少锁的争用。`Synced` 结构体包含队列的头和尾指针，以及一个标志位 `is_closed`，用于指示队列是否已关闭。`push` 和 `pop` 方法使用原子操作和指针操作来安全地添加和移除任务。

**与其他组件的交互：**

*   `task::Notified<T>`：表示已准备好执行的任务。
*   `Pop`：一个迭代器，用于从队列中弹出多个任务。
*   `loom::sync::atomic`：用于实现原子操作，确保线程安全。

**总结：**

这个文件定义了 Tokio 运行时中任务注入队列的共享状态，它使用原子操作和指针操作来实现线程安全，并与 `Synced` 结构体协同工作。
