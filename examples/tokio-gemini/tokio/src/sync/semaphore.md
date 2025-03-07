这个文件定义了 `tokio` 库中的 `Semaphore`（信号量）结构体及其相关的 `SemaphorePermit` 和 `OwnedSemaphorePermit` 类型。信号量是一种同步原语，用于限制对共享资源的并发访问数量。

**主要组成部分：**

*   **`Semaphore` 结构体：**
    *   `ll_sem`:  一个低级信号量的实现，用于处理底层的信号量操作。
    *   `resource_span`:  一个 `tracing::Span`，用于在启用 `tracing` 功能时，提供关于信号量资源的跟踪信息。
    *   `MAX_PERMITS`:  一个常量，表示信号量可以持有的最大许可数量。
    *   `new(permits: usize)`:  创建一个新的信号量，并初始化其许可数量。如果 `permits` 超过 `MAX_PERMITS`，则会 panic。
    *   `const_new(permits: usize)`:  创建一个新的信号量，但不会进行跟踪，适用于静态初始化。
    *   `new_closed()`:  创建一个关闭的信号量，初始许可数量为 0。
    *   `const_new_closed()`:  创建一个关闭的信号量，初始许可数量为 0，适用于静态初始化。
    *   `available_permits()`:  返回当前可用的许可数量。
    *   `add_permits(n: usize)`:  增加信号量的许可数量。
    *   `forget_permits(n: usize)`:  减少信号量的许可数量，但不通知等待者。
    *   `acquire()`:  异步地获取一个许可。如果当前没有可用许可，则会等待，直到有许可被释放。
    *   `acquire_many(n: u32)`:  异步地获取多个许可。
    *   `try_acquire()`:  尝试获取一个许可。如果当前有可用许可，则立即返回；否则，返回错误。
    *   `try_acquire_many(n: u32)`:  尝试获取多个许可。
    *   `acquire_owned(self: Arc<Self>)`:  异步地获取一个许可，并返回一个 `OwnedSemaphorePermit`。需要使用 `Arc` 包裹信号量。
    *   `acquire_many_owned(self: Arc<Self>, n: u32)`:  异步地获取多个许可，并返回一个 `OwnedSemaphorePermit`。需要使用 `Arc` 包裹信号量。
    *   `try_acquire_owned(self: Arc<Self>)`:  尝试获取一个许可，并返回一个 `OwnedSemaphorePermit`。需要使用 `Arc` 包裹信号量。
    *   `try_acquire_many_owned(self: Arc<Self>, n: u32)`:  尝试获取多个许可，并返回一个 `OwnedSemaphorePermit`。需要使用 `Arc` 包裹信号量。
    *   `close()`:  关闭信号量，阻止新的许可被获取，并通知所有等待者。
    *   `is_closed()`:  检查信号量是否已关闭。

*   **`SemaphorePermit` 结构体：**
    *   表示从信号量获取的许可。
    *   `forget()`:  忘记许可，不将其释放回信号量。
    *   `merge(other: Self)`:  合并两个 `SemaphorePermit` 实例。
    *   `split(n: usize)`:  从当前许可中拆分出 `n` 个许可。
    *   `num_permits()`:  返回当前许可持有的许可数量。
    *   `Drop` 实现：当 `SemaphorePermit` 离开作用域时，会将许可释放回信号量。

*   **`OwnedSemaphorePermit` 结构体：**
    *   表示从信号量获取的许可，并拥有信号量的所有权。
    *   `forget()`:  忘记许可，不将其释放回信号量。
    *   `merge(other: Self)`:  合并两个 `OwnedSemaphorePermit` 实例。
    *   `split(n: usize)`:  从当前许可中拆分出 `n` 个许可。
    *   `semaphore()`:  返回获取许可的信号量的 `Arc` 引用。
    *   `num_permits()`:  返回当前许可持有的许可数量。
    *   `Drop` 实现：当 `OwnedSemaphorePermit` 离开作用域时，会将许可释放回信号量。

**功能和作用：**

*   **限制并发：**  `Semaphore` 用于限制对共享资源的并发访问数量。通过获取和释放许可，可以控制同时访问资源的线程或任务的数量。
*   **公平性：**  `Semaphore` 保证了公平性，即按照请求的顺序发放许可。
*   **异步操作：**  `acquire` 和 `acquire_many` 方法是异步的，允许在没有可用许可时进行等待，而不会阻塞当前线程。
*   **错误处理：**  `acquire` 和 `acquire_many` 方法返回 `Result`，可以处理信号量关闭等错误情况。
*   **所有权：**  `acquire_owned` 和 `acquire_many_owned` 方法允许将信号量的所有权传递给其他线程或任务。
*   **多种使用场景：**  代码中提供了多种使用场景的示例，包括限制同时打开的文件数量、限制并发的请求数量、限制同时处理的请求数量以及防止测试并行运行等。
