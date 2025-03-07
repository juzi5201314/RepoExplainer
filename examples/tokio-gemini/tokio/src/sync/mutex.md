这个文件定义了 Tokio 异步编程框架中的 `Mutex` 类型，它类似于标准库中的 `std::sync::Mutex`，但主要区别在于 `lock` 方法是异步的，并且锁守卫设计为可以在 `.await` 点之间持有。

**主要组成部分：**

1.  **`Mutex<T>` 结构体：**
    *   `s: semaphore::Semaphore`：一个信号量，用于控制对互斥量的访问。
    *   `c: UnsafeCell<T>`：一个 `UnsafeCell`，用于安全地存储被保护的数据 `T`。
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：可选的追踪 `Span`，用于性能分析和调试（如果启用了 `tokio_unstable` 和 `tracing` 特性）。

2.  **`MutexGuard<'a, T>` 结构体：**
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：可选的追踪 `Span`。
    *   `lock: &'a Mutex<T>`：对 `Mutex` 的引用，表示持有锁。
    *   当 `MutexGuard` 被 drop 时，锁会被释放。

3.  **`OwnedMutexGuard<T>` 结构体：**
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：可选的追踪 `Span`。
    *   `lock: Arc<Mutex<T>>`：对 `Mutex` 的 `Arc` 引用，表示持有锁。
    *   与 `MutexGuard` 类似，但持有的是 `Arc`，因此可以跨线程使用，并且生命周期为 `'static`。

4.  **`MappedMutexGuard<'a, T>` 结构体：**
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：可选的追踪 `Span`。
    *   `s: &'a semaphore::Semaphore`：对信号量的引用。
    *   `data: *mut T`：指向被保护数据的子字段的原始指针。
    *   `marker: PhantomData<&'a mut T>`：用于借用检查器。
    *   允许访问被保护数据的子字段。

5.  **`OwnedMappedMutexGuard<T, U>` 结构体：**
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：可选的追踪 `Span`。
    *   `data: *mut U`：指向被保护数据的子字段的原始指针。
    *   `lock: Arc<Mutex<T>>`：对 `Mutex` 的 `Arc` 引用。
    *   与 `MappedMutexGuard` 类似，但持有的是 `Arc`，因此可以跨线程使用。

6.  **`TryLockError` 结构体：**
    *   表示 `try_lock` 操作失败的错误，即互斥锁已经被其他任务持有。

**关键方法：**

*   `new(t: T)`：创建一个新的 `Mutex`。
*   `const_new(t: T)`：创建一个新的 `Mutex`，用于 `const` 上下文（如果启用了 `loom` 特性）。
*   `lock()`：异步地获取锁，返回 `MutexGuard`。
*   `blocking_lock()`：同步地获取锁，返回 `MutexGuard`。
*   `lock_owned()`：异步地获取锁，返回 `OwnedMutexGuard`。
*   `blocking_lock_owned()`：同步地获取锁，返回 `OwnedMutexGuard`。
*   `try_lock()`：尝试获取锁，如果锁不可用则返回 `TryLockError`。
*   `try_lock_owned()`：尝试获取锁，如果锁不可用则返回 `TryLockError`。
*   `get_mut()`：获取对底层数据的可变引用（在没有锁的情况下）。
*   `into_inner()`：消费 `Mutex` 并返回底层数据。
*   `map()`：在 `MutexGuard` 或 `OwnedMutexGuard` 上创建一个 `MappedMutexGuard` 或 `OwnedMappedMutexGuard`，用于访问被保护数据的子字段。
*   `try_map()`：尝试创建 `MappedMutexGuard` 或 `OwnedMappedMutexGuard`，如果闭包返回 `None`，则返回原始的 guard。

**功能和作用：**

`Mutex` 提供了在 Tokio 异步运行时中安全地共享可变状态的机制。它允许任务异步地获取锁，并在 `.await` 点之间持有锁，从而避免了阻塞。`MutexGuard` 和 `OwnedMutexGuard` 确保了在锁被释放之前，对底层数据的独占访问。`MappedMutexGuard` 和 `OwnedMappedMutexGuard` 允许安全地访问被保护数据的子字段。
