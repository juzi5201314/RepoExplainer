这个文件定义了 `OwnedRwLockMappedWriteGuard` 结构体，它是一个拥有所有权的 RAII 结构，用于在被丢弃时释放对读写锁的独占写访问。它通过对 [`OwnedRwLockWriteGuard`] 进行 [mapping] 操作创建。与 `OwnedRwLockWriteGuard` 分开定义是为了禁止降级映射的 guard，因为这样做可能导致未定义行为。

**关键组件：**

*   `OwnedRwLockMappedWriteGuard<T: ?Sized, U: ?Sized = T>`：结构体本身，包含以下字段：
    *   `resource_span` (可选，仅在 `tokio_unstable` 和 `tracing` 特性启用时存在)：用于跟踪资源。
    *   `permits_acquired`：获取的许可数量。
    *   `lock`：指向 `RwLock<T>` 的 `Arc`。
    *   `data`：指向被锁数据的指针。
    *   `_p`：`PhantomData<T>`，用于类型安全。
*   `Inner<T: ?Sized, U: ?Sized>`：一个内部结构体，用于在 `skip_drop` 方法中安全地复制 `OwnedRwLockMappedWriteGuard` 的字段，避免在 drop 时出现问题。
*   `skip_drop(self) -> Inner<T, U>`：一个私有方法，用于将 `OwnedRwLockMappedWriteGuard` 的字段复制到一个 `Inner` 结构体中，并忘记原始的 `OwnedRwLockMappedWriteGuard`，从而避免在 drop 时释放锁。
*   `map<F, V: ?Sized>(mut this: Self, f: F) -> OwnedRwLockMappedWriteGuard<T, V>`：一个关联函数，用于创建一个新的 `OwnedRwLockMappedWriteGuard`，该 guard 引用了被锁数据的某个组件。它接受一个闭包 `f`，该闭包将对被锁数据的一个可变引用转换为对组件的可变引用。
*   `try_map<F, V: ?Sized>(mut this: Self, f: F) -> Result<OwnedRwLockMappedWriteGuard<T, V>, Self>`：一个关联函数，类似于 `map`，但如果闭包 `f` 返回 `None`，则返回原始的 guard。
*   `rwlock(this: &Self) -> &Arc<RwLock<T>>`：返回对原始 `Arc<RwLock>` 的引用。
*   `ops::Deref` 和 `ops::DerefMut` 的实现：允许通过 `*` 运算符访问和修改被锁数据。
*   `fmt::Debug` 和 `fmt::Display` 的实现：允许对 guard 进行调试和显示。
*   `Drop` 的实现：当 `OwnedRwLockMappedWriteGuard` 被丢弃时，它会释放锁。

**与其他组件的关系：**

*   与 `RwLock`：`OwnedRwLockMappedWriteGuard` 依赖于 `RwLock`，它持有对 `RwLock` 的引用。
*   与 `OwnedRwLockWriteGuard`：`OwnedRwLockMappedWriteGuard` 是通过对 `OwnedRwLockWriteGuard` 进行 mapping 操作创建的。
*   与 `map` 和 `try_map`：这两个方法允许在已经获取写锁的情况下，安全地访问和修改被锁数据的子部分。
