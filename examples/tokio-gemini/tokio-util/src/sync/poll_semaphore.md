这个文件定义了一个名为 `PollSemaphore` 的结构体，它是一个对 `tokio::sync::Semaphore` 的封装，提供了非阻塞的 `poll_acquire` 方法。`PollSemaphore` 允许在不阻塞当前线程的情况下尝试获取信号量许可。

**主要组成部分：**

*   **`PollSemaphore` 结构体:**
    *   `semaphore`:  一个 `Arc<Semaphore>`，持有底层的 `tokio::sync::Semaphore` 实例。使用 `Arc` 允许多个 `PollSemaphore` 实例共享同一个信号量。
    *   `permit_fut`:  一个 `Option`，包含一个元组，用于存储正在进行的获取许可的 Future。元组包含：
        *   `u32`:  请求的许可数量。
        *   `ReusableBoxFuture<'static, Result<OwnedSemaphorePermit, AcquireError>>`:  一个可重用的 Future，用于异步获取许可。`ReusableBoxFuture` 优化了 Future 的分配，避免了在每次 `poll_acquire` 调用时都进行分配。
*   **方法:**
    *   `new(semaphore: Arc<Semaphore>)`:  构造函数，创建一个新的 `PollSemaphore` 实例。
    *   `close(&self)`:  关闭底层的信号量。
    *   `clone_inner(&self)`:  返回底层信号量的克隆。
    *   `into_inner(self)`:  获取底层信号量的所有权。
    *   `poll_acquire(&mut self, cx: &mut Context<'_>) -> Poll<Option<OwnedSemaphorePermit>>`:  尝试获取一个许可。如果许可立即可用，则返回 `Poll::Ready(Some(permit))`。如果信号量已关闭，则返回 `Poll::Ready(None)`。如果许可不可用，则返回 `Poll::Pending`，并将当前任务注册到信号量，以便在许可可用时被唤醒。
    *   `poll_acquire_many(&mut self, cx: &mut Context<'_>, permits: u32) -> Poll<Option<OwnedSemaphorePermit>>`:  尝试获取多个许可。其行为类似于 `poll_acquire`，但可以请求多个许可。
    *   `available_permits(&self) -> usize`:  返回当前可用的许可数量。
    *   `add_permits(&self, n: usize)`:  向信号量添加新的许可。
*   **`Stream` trait 实现:**  `PollSemaphore` 实现了 `futures_core::Stream` trait，允许将其用作异步流。`poll_next` 方法调用 `poll_acquire` 来获取许可。
*   **`Clone` trait 实现:**  `PollSemaphore` 实现了 `Clone` trait，允许创建 `PollSemaphore` 实例的克隆，共享底层的信号量。
*   **`fmt::Debug` trait 实现:**  实现了 `Debug` trait，方便调试。
*   **`AsRef<Semaphore>` trait 实现:** 允许将 `PollSemaphore` 实例视为 `Semaphore` 引用。

**工作原理：**

`PollSemaphore` 通过 `poll_acquire` 和 `poll_acquire_many` 方法提供了非阻塞的信号量获取。当调用这些方法时，它首先尝试立即获取许可。如果许可不可用，它会创建一个 Future 来异步获取许可。这个 Future 会在后台等待许可可用，并在许可可用时完成。`PollSemaphore` 使用 `ReusableBoxFuture` 来优化 Future 的分配，避免了不必要的内存分配。当 Future 正在等待许可时，`poll_acquire` 方法会返回 `Poll::Pending`，并将当前任务的 `Waker` 注册到信号量，以便在许可可用时被唤醒。

**与其他组件的关联：**

*   **`tokio::sync::Semaphore`:**  `PollSemaphore` 封装了 `tokio::sync::Semaphore`，提供了非阻塞的接口。
*   **`futures_core::Stream`:**  `PollSemaphore` 实现了 `Stream` trait，使其可以与异步流一起使用。
*   **`ReusableBoxFuture`:**  用于优化 Future 的分配，提高性能。
