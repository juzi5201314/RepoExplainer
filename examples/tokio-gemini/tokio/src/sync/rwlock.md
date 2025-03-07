这个文件定义了 `tokio` 库中的异步读写锁 `RwLock` 及其相关类型和实现。`RwLock` 允许多个读者或一个写者同时访问共享数据，提供了比 `Mutex` 更高的并发性能。

**主要组成部分：**

1.  **`RwLock<T>` 结构体：**
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：用于追踪和调试，如果启用了 `tracing` 特性，则包含一个 `tracing::Span`。
    *   `mr: u32`：最大并发读者的数量。
    *   `s: Semaphore`：一个信号量，用于协调对 `T` 的读写访问。它控制了读写锁的并发访问。
    *   `c: UnsafeCell<T>`：包含实际数据的 `UnsafeCell`。使用 `UnsafeCell` 是因为 `RwLock` 允许多个读者并发访问数据，而 `UnsafeCell` 允许在没有 `&mut` 引用的情况下访问数据。

2.  **相关类型：**
    *   `owned_read_guard`、`owned_write_guard`、`owned_write_guard_mapped`、`read_guard`、`write_guard`、`write_guard_mapped`：这些模块定义了 `RwLock` 的 RAII 守卫，用于管理读写锁的生命周期。
    *   `OwnedRwLockReadGuard`、`OwnedRwLockWriteGuard`、`OwnedRwLockMappedWriteGuard`、`RwLockReadGuard`、`RwLockWriteGuard`、`RwLockMappedWriteGuard`：这些是 `RwLock` 的 RAII 守卫类型，分别对应于拥有锁的读访问、写访问，以及映射的写访问。

3.  **常量：**
    *   `MAX_READS: u32`：定义了最大并发读者的数量。在非 `loom` 环境下，其值为 `u32::MAX >> 3`，而在 `loom` 环境下，其值为 10。

4.  **`impl<T: ?Sized> RwLock<T>`：**
    *   `new(value: T)`：创建一个新的 `RwLock` 实例，并初始化数据。
    *   `with_max_readers(value: T, max_reads: u32)`：创建一个新的 `RwLock` 实例，并设置最大并发读者数量。
    *   `const_new(value: T)` 和 `const_with_max_readers(value: T, max_reads: u32)`：用于创建 `const` 类型的 `RwLock`，在编译时初始化。
    *   `read()`：异步获取读锁。
    *   `blocking_read()`：同步获取读锁。
    *   `read_owned()`：异步获取读锁，返回一个拥有锁的守卫，该守卫通过 `Arc` 引用 `RwLock`。
    *   `try_read()`：尝试获取读锁，如果立即获取失败，则返回 `TryLockError`。
    *   `try_read_owned()`：尝试获取读锁，返回一个拥有锁的守卫，该守卫通过 `Arc` 引用 `RwLock`。
    *   `write()`：异步获取写锁。
    *   `blocking_write()`：同步获取写锁。
    *   `write_owned()`：异步获取写锁，返回一个拥有锁的守卫，该守卫通过 `Arc` 引用 `RwLock`。
    *   `try_write()`：尝试获取写锁，如果立即获取失败，则返回 `TryLockError`。
    *   `try_write_owned()`：尝试获取写锁，返回一个拥有锁的守卫，该守卫通过 `Arc` 引用 `RwLock`。
    *   `get_mut()`：获取对底层数据的可变引用，绕过锁机制，仅在静态保证没有其他锁存在时使用。
    *   `into_inner()`：消耗锁，返回底层数据。

5.  **`impl From<T> for RwLock<T>` 和 `impl Default for RwLock<T>`：** 实现了 `From` 和 `Default` trait，方便创建和初始化 `RwLock`。

6.  **`impl std::fmt::Debug for RwLock<T>`：** 实现了 `Debug` trait，方便调试。

7.  **`unsafe impl` 块：** 定义了 `Send` 和 `Sync` trait 的实现，确保 `RwLock` 及其守卫可以在多线程环境中安全使用。

**功能和作用：**

该文件定义了 `tokio` 库中异步读写锁的核心实现，为并发编程提供了重要的同步原语。`RwLock` 允许更细粒度的并发控制，允许多个读者同时访问数据，从而提高性能。它通过信号量来协调读写操作，并使用 RAII 守卫来管理锁的生命周期，确保了线程安全和资源管理。
