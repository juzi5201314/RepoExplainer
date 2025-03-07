这个文件定义了 `Notify` 结构体及其相关的辅助结构体和实现，用于在 Tokio 运行时中实现任务间的通知和同步。

**主要组件：**

*   **`Notify`**:  核心结构体，用于通知单个任务。它类似于一个信号量，初始值为 0。`notified().await` 方法等待一个“许可”可用，而 `notify_one()` 方法设置一个“许可”。
    *   `state`:  一个 `AtomicUsize`，使用 2 位来存储 `EMPTY`、`WAITING` 或 `NOTIFIED` 状态。其余位用于存储 `notify_waiters` 被调用的次数。
    *   `waiters`:  一个 `Mutex<WaitList>`，用于存储等待通知的任务的列表。
*   **`Waiter`**:  表示一个等待通知的任务。
    *   `pointers`:  用于链表操作的指针。
    *   `waker`:  一个 `UnsafeCell<Option<Waker>>`，存储任务的 `Waker`，用于唤醒任务。
    *   `notification`:  一个 `AtomicNotification`，用于原子地存储通知状态。
    *   `_p`:  `PhantomPinned`，确保 `Waiter` 不可 `Unpin`。
*   **`AtomicNotification`**:  用于原子地存储通知状态的结构体。
*   **`Notification`**:  一个枚举，表示通知的类型，可以是 `One` (使用 FIFO 或 LIFO 策略通知一个等待者) 或 `All` (通知所有等待者)。
*   **`NotifyOneStrategy`**:  一个枚举，表示 `notify_one` 使用的策略，FIFO 或 LIFO。
*   **`NotifyWaitersList`**:  一个辅助结构体，用于在 `notify_waiters` 中管理等待者列表。
*   **`Notified`**:  `Notify::notified()` 方法返回的 Future。当被轮询时，它会尝试接收通知。
    *   `notify`:  对 `Notify` 实例的引用。
    *   `state`:  当前状态，`Init`, `Waiting`, 或 `Done`。
    *   `notify_waiters_calls`:  创建时 `notify_waiters` 被调用的次数。
    *   `waiter`:  `Waiter` 实例。
*   **`State`**:  `Notified` future 的状态。
*   常量：`EMPTY`, `WAITING`, `NOTIFIED`, `NOTIFICATION_NONE`, `NOTIFICATION_ONE`, `NOTIFICATION_LAST`, `NOTIFICATION_ALL` 等，用于表示状态和通知类型。

**功能和工作原理：**

1.  **`Notify::new()`**:  创建一个新的 `Notify` 实例。
2.  **`Notify::notified()`**:  创建一个 `Notified` future，用于等待通知。
3.  **`Notify::notify_one()`**:  通知一个等待的任务。如果当前没有等待的任务，则存储一个“许可”。
4.  **`Notify::notify_last()`**:  通知最后一个等待的任务 (LIFO)。
5.  **`Notify::notify_waiters()`**:  通知所有等待的任务。
6.  **`Notified::poll()`**:  轮询 `Notified` future。如果已经收到通知，则返回 `Poll::Ready`。否则，将当前任务的 `Waker` 注册到 `Notify` 的等待者列表中，并返回 `Poll::Pending`。
7.  **`Notified::enable()`**:  将 future 添加到等待列表中，即使尚未被轮询。

**与其他组件的交互：**

*   `Notify` 与 Tokio 运行时紧密集成，用于任务间的同步。
*   `Notified` future 用于等待来自 `Notify` 的通知。
*   `Waiter` 结构体用于存储等待通知的任务的信息。
*   `Mutex` 用于保护对等待者列表的访问。
*   `AtomicUsize` 用于原子地更新状态。
*   `LinkedList` 用于管理等待者列表。

**代码示例：**

该文件包含多个代码示例，展示了 `Notify` 在不同场景下的使用，例如：

*   基本用法：一个任务等待另一个任务发送通知。
*   无界多生产者单消费者 (mpsc) 频道。
*   无界多生产者多消费者 (mpmc) 频道。

**总结：**

这个文件定义了 `Notify` 结构体，它提供了一种轻量级的机制，用于在 Tokio 运行时中实现任务间的通知和同步。它类似于一个信号量，但更专注于通知单个任务。`Notify` 及其相关的结构体和方法，为构建并发应用程序提供了重要的基础。
