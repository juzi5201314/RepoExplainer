这个文件定义了与 `TaskTracker` 集合相关的类型，`TaskTracker` 用于跟踪和等待异步任务的退出。它主要用于实现优雅的关闭，例如与 `CancellationToken` 结合使用。

**关键组件：**

*   **`TaskTracker`**:  一个结构体，用于跟踪异步任务。它使用 `Arc<TaskTrackerInner>` 来允许多个任务共享跟踪器。
    *   `new()`: 创建一个新的 `TaskTracker`。
    *   `wait()`: 返回一个 `TaskTrackerWaitFuture`，该 future 在 `TaskTracker` 关闭且所有跟踪的任务都退出时完成。
    *   `close()`: 关闭 `TaskTracker`，允许 `wait` future 完成。
    *   `reopen()`: 重新打开 `TaskTracker`，阻止 `wait` future 完成。
    *   `is_closed()`:  如果 `TaskTracker` 已关闭，则返回 `true`。
    *   `len()`: 返回 `TaskTracker` 中跟踪的任务数量。
    *   `is_empty()`:  如果 `TaskTracker` 中没有任务，则返回 `true`。
    *   `spawn()`/`spawn_on()`/`spawn_local()`/`spawn_local_on()`/`spawn_blocking()`/`spawn_blocking_on()`:  在 Tokio 运行时上生成任务，并使用 `track_future` 跟踪它们。
    *   `track_future()`:  跟踪给定的 future，返回一个 `TrackedFuture`。
    *   `token()`: 创建一个 `TaskTrackerToken`，表示一个被 `TaskTracker` 跟踪的任务。
    *   `ptr_eq()`: 检查两个 `TaskTracker` 是否指向相同的内部状态。
    *   `clone()`: 创建 `TaskTracker` 的一个克隆。
*   **`TaskTrackerToken`**:  一个结构体，表示由 `TaskTracker` 跟踪的任务。当 `TaskTrackerToken` 被 drop 时，它会通知 `TaskTracker` 对应的任务已经退出。
    *   `task_tracker()`:  返回与此 token 关联的 `TaskTracker`。
    *   `clone()`:  创建一个新的 `TaskTrackerToken`，与原始 token 关联到同一个 `TaskTracker`。
*   **`TaskTrackerInner`**:  `TaskTracker` 的内部结构，包含原子状态和通知机制。
    *   `state`:  一个原子整数，用于跟踪 `TaskTracker` 的状态（是否关闭，跟踪的任务数量）。
    *   `on_last_exit`:  一个 `Notify`，用于在最后一个任务退出时通知等待者。
    *   `new()`: 创建一个新的 `TaskTrackerInner`。
    *   `is_closed_and_empty()`: 检查 `TaskTracker` 是否已关闭且为空。
    *   `set_closed()`:  设置 `TaskTracker` 为关闭状态。
    *   `set_open()`:  设置 `TaskTracker` 为打开状态。
    *   `add_task()`:  增加跟踪的任务计数。
    *   `drop_task()`:  减少跟踪的任务计数。
    *   `notify_now()`:  通知等待者。
*   **`TrackedFuture<F>`**:  一个 future，它包装了另一个 future，并由 `TaskTracker` 跟踪。当 `TrackedFuture` 被 drop 时，它会通知 `TaskTracker` 对应的任务已经退出。
*   **`TaskTrackerWaitFuture<'a>`**:  一个 future，它在 `TaskTracker` 关闭且所有跟踪的任务都退出时完成。

**工作原理：**

1.  `TaskTracker` 跟踪任务的数量和是否关闭的状态。
2.  当一个任务被跟踪时，会创建一个 `TaskTrackerToken`，增加任务计数。
3.  当一个任务完成时，`TaskTrackerToken` 被 drop，减少任务计数。
4.  `close()` 方法设置 `TaskTracker` 为关闭状态。
5.  `wait()` 方法返回一个 future，该 future 在 `TaskTracker` 关闭且任务计数为 0 时完成。

**与其他组件的关系：**

*   与 `CancellationToken` 结合使用，实现优雅的关闭。
*   与 Tokio 的运行时交互，通过 `spawn` 系列方法生成和跟踪任务。
