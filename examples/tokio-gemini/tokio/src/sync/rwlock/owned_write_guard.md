这个文件定义了 `OwnedRwLockWriteGuard` 结构体，它是一个拥有所有权的 RAII 结构，用于在被释放时释放对 `RwLock` 的独占写访问。

**关键组件：**

*   `OwnedRwLockWriteGuard<T>`：这个结构体代表了对 `RwLock<T>` 的独占写访问。它包含以下字段：
    *   `resource_span` (可选，当 `tokio_unstable` 和 `tracing` 特性启用时)：用于跟踪资源使用情况的 `tracing::Span`。
    *   `permits_acquired`：表示获取的许可数量。
    *   `lock`：指向 `RwLock<T>` 的 `Arc`。
    *   `data`：指向被锁定的数据的原始指针。
    *   `_p`：一个 `PhantomData<T>`，用于确保类型安全。
*   `Inner<T>`：一个内部结构体，用于在 `skip_drop` 方法中避免在 drop 时重复释放锁。
*   `skip_drop`：一个私有方法，用于创建一个 `Inner` 实例，从而避免在 `OwnedRwLockWriteGuard` 被移动时释放锁。
*   `map`：允许创建一个 `OwnedRwLockMappedWriteGuard`，用于访问被锁定数据的特定部分。
*   `downgrade_map`：允许将写锁降级为读锁，并映射到数据的特定部分，返回 `OwnedRwLockReadGuard`。
*   `try_map`：尝试创建一个 `OwnedRwLockMappedWriteGuard`，如果闭包返回 `None`，则返回原始的 `OwnedRwLockWriteGuard`。
*   `try_downgrade_map`：尝试将写锁降级为读锁，并映射到数据的特定部分，如果闭包返回 `None`，则返回原始的 `OwnedRwLockWriteGuard`。
*   `into_mapped`：将 `OwnedRwLockWriteGuard` 转换为 `OwnedRwLockMappedWriteGuard`。
*   `downgrade`：将写锁原子地降级为读锁，返回 `OwnedRwLockReadGuard`。
*   `rwlock`：返回对原始 `RwLock` 的引用。
*   `Deref` 和 `DerefMut` 的实现：允许像访问普通引用一样访问被锁定的数据。
*   `Debug` 和 `Display` 的实现：允许调试和显示被锁定的数据。
*   `Drop` 的实现：当 `OwnedRwLockWriteGuard` 离开作用域时，释放对锁的独占写访问。

**功能：**

*   **独占写访问：** `OwnedRwLockWriteGuard` 确保在任何时候只有一个线程可以写入被保护的数据。
*   **RAII：** 通过在 `Drop` 实现中释放锁，确保即使发生 panic，锁也会被正确释放。
*   **映射：** 允许创建指向被锁定数据特定部分的 guard，从而实现更细粒度的访问控制。
*   **降级：** 允许将写锁降级为读锁，从而允许多个线程同时读取数据。
*   **原子性：** `downgrade` 操作是原子的，确保在降级过程中没有其他线程可以获取写锁。

**与其他组件的交互：**

*   与 `RwLock` 交互：`OwnedRwLockWriteGuard` 是通过 `RwLock` 的 `write_owned` 方法创建的。
*   与 `OwnedRwLockReadGuard` 交互：`downgrade` 和 `try_downgrade_map` 方法将写锁转换为读锁，返回 `OwnedRwLockReadGuard`。
*   与 `OwnedRwLockMappedWriteGuard` 交互：`map` 和 `try_map` 方法创建 `OwnedRwLockMappedWriteGuard`。
