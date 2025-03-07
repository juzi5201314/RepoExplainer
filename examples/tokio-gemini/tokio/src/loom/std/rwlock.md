这个文件定义了一个名为 `RwLock` 的结构体，它是标准库 `std::sync::RwLock` 的一个适配器，移除了其 API 中的中毒（poisoning）特性。

**主要组成部分：**

1.  **`use` 语句：** 导入了 `std::sync` 模块中的相关类型，包括 `RwLockReadGuard`, `RwLockWriteGuard`, 和 `TryLockError`。
2.  **`RwLock` 结构体：**
    *   `pub(crate) struct RwLock<T: ?Sized>(sync::RwLock<T>)`：定义了一个泛型结构体 `RwLock`，它内部包含一个标准库的 `sync::RwLock` 实例。`?Sized` 约束允许 `T` 是一个动态大小的类型。`pub(crate)` 意味着该结构体在当前 crate 内可见。
3.  **`impl<T> RwLock<T>` 块：** 实现了 `RwLock` 结构体的方法。
    *   `new(t: T) -> Self`：构造函数，创建一个新的 `RwLock` 实例，并用给定的值 `t` 初始化内部的 `sync::RwLock`。
    *   `read(&self) -> RwLockReadGuard<'_, T>`：获取一个只读锁。如果底层 `RwLock` 发生了中毒，则会解毒（unpoison）并返回一个只读锁。
    *   `try_read(&self) -> Option<RwLockReadGuard<'_, T>>`：尝试获取一个只读锁。如果成功，则返回 `Some(RwLockReadGuard)`；如果锁已被占用，则返回 `None`；如果底层 `RwLock` 发生了中毒，则会解毒并返回一个只读锁。
    *   `write(&self) -> RwLockWriteGuard<'_, T>`：获取一个写锁。如果底层 `RwLock` 发生了中毒，则会解毒并返回一个写锁。
    *   `try_write(&self) -> Option<RwLockWriteGuard<'_, T>>`：尝试获取一个写锁。如果成功，则返回 `Some(RwLockWriteGuard)`；如果锁已被占用，则返回 `None`；如果底层 `RwLock` 发生了中毒，则会解毒并返回一个写锁。

**功能和作用：**

这个文件提供了一个线程安全的读写锁的实现，它包装了标准库的 `RwLock`，并移除了中毒特性。这意味着即使在锁被持有期间发生 panic，后续的锁操作也不会因为中毒而失败。这使得 `RwLock` 在多线程环境中更加健壮和易于使用。

**与项目的关系：**
