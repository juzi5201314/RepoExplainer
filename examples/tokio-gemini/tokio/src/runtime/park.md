这个文件定义了 `ParkThread` 和 `UnparkThread` 结构体，它们用于在 Tokio 运行时中实现线程的阻塞和唤醒机制。它还包含一个 `CachedParkThread` 结构体，用于提供一个线程本地的 `ParkThread` 实例，并提供 `park` 和 `park_timeout` 方法。

**关键组件：**

*   **`ParkThread`**:
    *   用于阻塞当前线程。
    *   包含一个 `Inner` 类型的 `Arc` 引用，用于共享状态。
    *   `new()`: 创建一个新的 `ParkThread` 实例。
    *   `unpark()`: 返回一个 `UnparkThread` 实例，用于唤醒线程。
    *   `park()`: 阻塞当前线程，直到被唤醒。
    *   `park_timeout(duration)`: 阻塞当前线程，直到被唤醒或超时。
    *   `shutdown()`: 唤醒所有等待的线程。
*   **`UnparkThread`**:
    *   用于唤醒被 `ParkThread` 阻塞的线程。
    *   包含一个 `Inner` 类型的 `Arc` 引用，与 `ParkThread` 共享状态。
    *   `unpark()`: 唤醒被阻塞的线程。
*   **`Inner`**:
    *   包含线程阻塞和唤醒的核心逻辑。
    *   `state`: 使用 `AtomicUsize` 存储线程状态（EMPTY, PARKED, NOTIFIED）。
    *   `mutex`: 使用 `Mutex` 保护状态的访问。
    *   `condvar`: 使用 `Condvar` 实现线程的等待和通知。
    *   `park()`: 阻塞当前线程，直到被唤醒。
    *   `park_timeout(duration)`: 阻塞当前线程，直到被唤醒或超时。
    *   `unpark()`: 唤醒被阻塞的线程。
    *   `shutdown()`: 唤醒所有等待的线程。
*   **`CachedParkThread`**:
    *   提供线程本地的 `ParkThread` 实例。
    *   `new()`: 创建一个新的 `CachedParkThread` 实例。
    *   `waker()`: 获取一个 `Waker`，用于唤醒线程。
    *   `park()`: 阻塞当前线程。
    *   `park_timeout(duration)`: 阻塞当前线程，直到被唤醒或超时。
    *   `block_on(f)`: 在当前线程上阻塞执行一个 `Future`。
*   **`CURRENT_PARKER`**:
    *   一个线程本地变量，存储当前线程的 `ParkThread` 实例。
*   **`CURRENT_THREAD_PARK_COUNT`**:
    *   一个线程本地变量，用于在 loom 测试中跟踪线程的 park 次数。
*   **状态常量**:
    *   `EMPTY`: 线程未被阻塞。
    *   `PARKED`: 线程已阻塞。
    *   `NOTIFIED`: 线程已被通知。

**工作原理：**

1.  `ParkThread` 通过 `Inner` 中的 `state`、`mutex` 和 `condvar` 来协调线程的阻塞和唤醒。
2.  `park()` 方法首先检查线程是否已经被通知（`NOTIFIED` 状态）。如果是，则立即返回。否则，它将线程状态设置为 `PARKED`，然后使用 `condvar.wait()` 阻塞线程。
3.  `unpark()` 方法将线程状态设置为 `NOTIFIED`，并使用 `condvar.notify_one()` 唤醒一个被阻塞的线程。
4.  `park_timeout()` 方法与 `park()` 类似，但它设置了一个超时时间。
5.  `CachedParkThread` 提供了一个线程本地的 `ParkThread` 实例，方便在 Tokio 运行时中使用。它还提供了 `block_on` 方法，用于在当前线程上阻塞执行一个 `Future`。

**与项目的关系：**

这个文件是 Tokio 运行时中实现线程阻塞和唤醒机制的核心部分。它为 Tokio 运行时提供了基础的并发原语，使得 Tokio 能够高效地调度和执行异步任务。`ParkThread` 和 `UnparkThread` 用于实现任务的挂起和恢复，是 Tokio 运行时实现异步执行的关键组件。
