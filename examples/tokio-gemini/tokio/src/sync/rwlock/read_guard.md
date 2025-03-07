这个文件定义了 `RwLockReadGuard` 结构体，它是一个用于管理读写锁（`RwLock`）的读访问的 RAII 结构体。它的主要目的是在读锁被获取后，确保在 `RwLockReadGuard` 离开作用域时，读锁被正确释放。

**关键组件：**

*   `RwLockReadGuard<'a, T>`：
    *   `s: &'a Semaphore`：指向用于管理读写锁的信号量（`Semaphore`）。当 `RwLockReadGuard` 被 `drop` 时，会调用信号量的 `release` 方法来释放读锁。
    *   `data: *const T`：指向被锁定的数据的指针。
    *   `marker: PhantomData<&'a T>`：一个零大小的标记，用于确保 `RwLockReadGuard` 拥有对数据的生命周期引用。
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`：可选的，用于追踪读锁的生命周期，如果启用了 `tokio_unstable` 和 `tracing` 特性。
*   `Inner<'a, T>`：一个内部结构体，用于在 `map` 和 `try_map` 方法中避免移动 `RwLockReadGuard` 时的潜在问题。
*   `skip_drop` 方法：创建一个 `Inner` 实例，用于在 `map` 和 `try_map` 方法中复制 `RwLockReadGuard` 的字段，然后忘记原始的 `RwLockReadGuard`，从而避免在移动 `RwLockReadGuard` 时调用 `drop`。
*   `map` 方法：允许创建一个新的 `RwLockReadGuard`，它指向被锁定数据的子组件。
*   `try_map` 方法：尝试创建一个新的 `RwLockReadGuard`，它指向被锁定数据的子组件。如果闭包返回 `None`，则返回原始的 `RwLockReadGuard`。
*   `Deref` 实现：允许通过 `*` 运算符访问被锁定的数据。
*   `Debug` 和 `Display` 实现：允许以调试和显示格式打印被锁定的数据。
*   `Drop` 实现：当 `RwLockReadGuard` 离开作用域时，释放读锁。它通过调用信号量的 `release` 方法来实现。

**与其他组件的交互：**

*   与 `Semaphore` 交互：`RwLockReadGuard` 使用 `Semaphore` 来管理读锁的获取和释放。在 `Drop` 实现中，它调用 `s.release(1)` 来释放读锁。
*   与 `RwLock` 交互：`RwLockReadGuard` 由 `RwLock` 的 `read` 方法创建。
*   与 `map` 和 `try_map` 方法交互：这些方法允许创建指向被锁定数据的子组件的新的 `RwLockReadGuard`。
