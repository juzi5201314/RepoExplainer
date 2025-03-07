这个文件定义了用于存储在调度器上生成的任务的容器。它主要包含两个结构体：`OwnedTasks` 和 `LocalOwnedTasks`。`OwnedTasks` 是线程安全的，但只能存储实现 `Send` trait 的任务。`LocalOwnedTasks` 不是线程安全的，但可以存储非 `Send` 任务。

**关键组件：**

*   **`OwnedTasks<S>`**:
    *   `list`: 使用 `sharded_list::ShardedList` 存储任务。`ShardedList` 是一种分片列表，用于减少并发访问时的锁争用。
    *   `id`:  一个唯一的 ID，用于标识此 `OwnedTasks` 实例。
    *   `closed`:  一个原子布尔值，表示该任务列表是否已关闭。当关闭时，不允许添加新任务。
    *   `new(num_cores: usize)`:  创建一个新的 `OwnedTasks` 实例，并根据核心数量设置分片列表的大小。
    *   `bind<T>(...)`:  将一个 `Send` 任务绑定到此 `OwnedTasks` 实例。
    *   `bind_local<T>(...)`:  将一个非 `Send` 任务绑定到此 `OwnedTasks` 实例。
    *   `assert_owner(...)`:  断言给定的任务属于此 `OwnedTasks` 实例。
    *   `close_and_shutdown_all(...)`:  关闭任务列表并关闭所有任务。
    *   `remove(...)`:  从列表中移除一个任务。
    *   `is_empty()`:  检查列表是否为空。
    *   `get_shard_size()`:  获取分片列表的大小。
    *   `num_alive_tasks()`:  获取存活任务的数量。
    *   `spawned_tasks_count()`:  获取已生成任务的数量 (仅在启用 64 位指标时可用)。
    *   `gen_shared_list_size(num_cores: usize)`:  根据核心数量生成分片列表的大小。

*   **`LocalOwnedTasks<S>`**:
    *   `inner`:  使用 `UnsafeCell` 包装的 `OwnedTasksInner`，用于存储任务列表。由于 `UnsafeCell` 不是线程安全的，因此 `LocalOwnedTasks` 也不是线程安全的。
    *   `id`:  一个唯一的 ID，用于标识此 `LocalOwnedTasks` 实例。
    *   `_not_send_or_sync`:  一个 `PhantomData` 标记，用于确保 `LocalOwnedTasks` 不实现 `Send` 和 `Sync` trait。
    *   `new()`:  创建一个新的 `LocalOwnedTasks` 实例。
    *   `bind<T>(...)`:  将一个任务绑定到此 `LocalOwnedTasks` 实例。
    *   `close_and_shutdown_all(...)`:  关闭任务列表并关闭所有任务。
    *   `remove(...)`:  从列表中移除一个任务。
    *   `assert_owner(...)`:  断言给定的任务属于此 `LocalOwnedTasks` 实例。
    *   `is_closed()`:  检查列表是否已关闭。
    *   `is_empty()`:  检查列表是否为空。
    *   `with_inner(...)`:  一个辅助方法，用于安全地访问 `inner` 中的数据。

*   **`OwnedTasksInner<S>`**:
    *   `list`:  使用 `LinkedList` 存储任务。
    *   `closed`:  一个布尔值，表示该任务列表是否已关闭。

*   **`get_next_id()`**:  用于生成唯一的任务列表 ID。

**工作原理：**

`OwnedTasks` 和 `LocalOwnedTasks` 充当任务的容器。当生成一个任务时，它会被绑定到其中一个容器。`OwnedTasks` 用于存储可以在线程之间安全传递的任务，而 `LocalOwnedTasks` 用于存储不能在线程之间传递的任务。当调度器关闭时，它会关闭这些容器，并关闭所有未完成的任务。

**与其他文件的关系：**

*   与 `crate::runtime::task` 模块交互，用于创建和管理任务。
*   使用 `crate::util::linked_list` 和 `crate::util::sharded_list` 来存储任务。
*   使用 `crate::loom::sync::atomic` 来实现线程安全的操作。
*   与调度器模块交互，用于管理任务的执行。
