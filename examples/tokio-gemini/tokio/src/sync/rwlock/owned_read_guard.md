这个文件定义了 `OwnedRwLockReadGuard` 结构体，它是一个拥有所有权的 RAII 结构，用于在 `tokio::sync::RwLock` 上进行共享读取访问。当这个结构体被 drop 时，它会释放锁。

**关键组件：**

*   `OwnedRwLockReadGuard<T: ?Sized, U: ?Sized = T>`:  这个结构体代表了对 `RwLock` 的共享读取访问。
    *   `lock: Arc<RwLock<T>>`:  持有对 `RwLock` 的 `Arc` 引用，用于管理锁的生命周期。
    *   `data: *const U`:  指向被锁定的数据的指针。 `U` 可以是 `T` 的一部分，允许对锁定的数据进行映射。
    *   `_p: PhantomData<T>`:  用于类型安全，确保 `T` 存在于结构体中，即使 `T` 没有被直接使用。
    *   `#[cfg(all(tokio_unstable, feature = "tracing"))] resource_span: tracing::Span`:  用于追踪，如果启用了 `tokio_unstable` 和 `tracing` 特性，则包含一个 `tracing::Span`。
*   `Inner<T: ?Sized, U: ?Sized>`:  一个内部结构体，用于在 `skip_drop` 方法中临时存储 `OwnedRwLockReadGuard` 的字段，避免在 `drop` 期间移动数据。
*   `skip_drop(self) -> Inner<T, U>`:  这个方法用于“跳过” `drop` 行为。它将 `OwnedRwLockReadGuard` 的字段复制到一个新的 `Inner` 结构体中，然后忘记原始的 `OwnedRwLockReadGuard`，从而避免在 `drop` 时释放锁。这主要用于 `map` 和 `try_map` 方法中，以避免在创建新的 guard 时过早地释放锁。
*   `map<F, V: ?Sized>(this: Self, f: F) -> OwnedRwLockReadGuard<T, V>`:  允许创建一个新的 `OwnedRwLockReadGuard`，它指向被锁定数据的子部分。`f` 是一个闭包，它接受对原始数据的引用，并返回对子部分的引用。
*   `try_map<F, V: ?Sized>(this: Self, f: F) -> Result<OwnedRwLockReadGuard<T, V>, Self>`:  类似于 `map`，但如果闭包 `f` 返回 `None`，则返回原始的 `OwnedRwLockReadGuard`，而不是创建一个新的 guard。
*   `rwlock(this: &Self) -> &Arc<RwLock<T>>`:  返回对原始 `RwLock` 的 `Arc` 引用。
*   `ops::Deref` 实现：允许通过 `*` 运算符访问被锁定的数据。
*   `fmt::Debug` 和 `fmt::Display` 实现：允许以调试和显示格式打印被锁定的数据。
*   `Drop` 实现：当 `OwnedRwLockReadGuard` 离开作用域时，它会调用 `lock.s.release(1)` 来释放共享读取锁。如果启用了 `tracing` 特性，还会记录一个追踪事件。

**与其他组件的交互：**

*   与 `RwLock` 交互：`OwnedRwLockReadGuard` 通过 `Arc<RwLock<T>>` 持有对 `RwLock` 的引用，并使用 `RwLock` 的内部机制来获取和释放锁。
*   与 `read_owned` 方法交互：`OwnedRwLockReadGuard` 是由 `RwLock` 的 `read_owned` 方法创建的。
*   与 `map` 和 `try_map` 方法交互：这些方法允许在已获取的锁上进行数据转换，并创建新的 `OwnedRwLockReadGuard` 来引用转换后的数据。
