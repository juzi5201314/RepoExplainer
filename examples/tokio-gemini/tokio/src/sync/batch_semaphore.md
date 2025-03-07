这个文件实现了 `tokio` 库中的一个异步计数信号量 `Semaphore`。它允许任务等待多个许可同时可用。

**主要组件：**

*   **`Semaphore` 结构体：** 这是信号量的核心。它包含：
    *   `waiters`: 一个互斥锁，保护等待者列表 `Waitlist`。
    *   `permits`: 一个原子计数器，跟踪信号量中可用的许可数量。
    *   `resource_span`: (可选，启用 `tracing` 特性时) 用于跟踪信号量资源。
*   **`Waitlist` 结构体：** 包含一个等待者队列 `LinkedList` 和一个表示信号量是否已关闭的标志 `closed`。
*   **`Waiter` 结构体：** 表示等待获取许可的任务。它包含：
    *   `state`: 一个原子计数器，表示等待者剩余需要的许可数量，或者表示等待者是否尚未排队。
    *   `waker`: 一个 `UnsafeCell`，包含用于唤醒等待任务的 `Waker`。
    *   `pointers`: 用于在链表中链接等待者的指针。
    *   `ctx`: (可选，启用 `tracing` 特性时) 用于跟踪异步操作的上下文。
    *   `_p`: `PhantomPinned` 确保 `Waiter` 不可 `Unpin`。
*   **`Acquire` 结构体：**  一个 `Future`，用于异步获取信号量许可。
*   **`TryAcquireError` 枚举：**  表示 `try_acquire` 函数可能返回的错误，包括 `Closed` (信号量已关闭) 和 `NoPermits` (没有可用的许可)。
*   **`AcquireError` 结构体：** 表示 `acquire` 函数可能返回的错误，目前仅包含 `closed`。

**功能：**

*   **`new(permits: usize)`:** 创建一个新的信号量，并初始化一定数量的许可。
*   **`const_new(permits: usize)`:** 创建一个新的信号量，在编译时初始化一定数量的许可。
*   **`new_closed()`:** 创建一个已关闭的信号量，初始许可数为 0。
*   **`const_new_closed()`:** 创建一个已关闭的信号量，在编译时初始化。
*   **`available_permits()`:** 返回当前可用的许可数量。
*   **`release(added: usize)`:** 释放指定数量的许可，将它们添加到信号量中，并唤醒等待者。
*   **`close()`:** 关闭信号量，阻止新的许可发放，并唤醒所有等待者。
*   **`is_closed()`:** 检查信号量是否已关闭。
*   **`try_acquire(num_permits: usize)`:** 尝试立即获取指定数量的许可。如果许可不足或信号量已关闭，则返回错误。
*   **`acquire(num_permits: usize)`:** 异步获取指定数量的许可。如果许可不足，则任务将被挂起，直到有足够的许可可用。
*   **`forget_permits(n: usize)`:** 减少信号量的许可数量，最多减少 `n`。
*   **`poll_acquire(cx: &mut Context<'_>, num_permits: usize, node: Pin<&mut Waiter>, queued: bool)`:**  `Acquire` Future 的轮询函数，处理获取许可的逻辑。
*   **`add_permits_locked(mut rem: usize, waiters: MutexGuard<'_, Waitlist>)`:**  将许可分配给等待者，从队列的末尾开始。

**工作原理：**

信号量使用一个等待者队列（基于侵入式链表）来管理等待获取许可的任务。当一个任务尝试获取许可时，如果许可不足，则将该任务的 `Waker` 放入队列。当新的许可可用时，它们被分配给队列中的任务，如果任务的请求被满足，则唤醒该任务。这种实现保证了公平性，避免了写者饥饿。

**与其他组件的交互：**

*   使用 `loom` 库进行并发测试。
*   使用 `tracing` 库进行跟踪（如果启用了 `tokio-unstable` 和 `tracing` 特性）。
*   与 `linked_list` 模块交互，用于管理等待者队列。
*   与 `Mutex` 互斥锁交互，保护等待者队列。
*   与 `AtomicUsize` 原子整数交互，用于管理许可计数。
*   与 `Future` 特性交互，实现异步获取许可。
