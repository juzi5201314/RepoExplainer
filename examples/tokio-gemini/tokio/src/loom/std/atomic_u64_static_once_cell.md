这个文件定义了 `StaticAtomicU64` 结构体，它模拟了静态的 64 位原子整数，并提供了一些原子操作。它主要用于在编译时初始化原子变量，这在某些情况下是必要的，例如在静态变量中使用原子变量。

**关键组件：**

*   **`StaticAtomicU64` 结构体:**
    *   `init: u64`：用于存储初始值的 `u64` 类型的字段。
    *   `cell: OnceCell<Mutex<u64>>`：使用 `OnceCell` 和 `Mutex` 来实现延迟初始化和线程安全。`OnceCell` 确保只初始化一次，`Mutex` 保护对底层 `u64` 值的访问。

*   **`AtomicU64` 结构体:**
    *   `inner: Mutex<u64>`：使用 `Mutex` 来包装 `u64`，提供线程安全。

*   **`new(val: u64)` (对于 `AtomicU64`):**  创建一个新的 `AtomicU64` 实例，使用给定的初始值。

*   **`new(val: u64)` (对于 `StaticAtomicU64`):**  创建一个新的 `StaticAtomicU64` 实例，使用给定的初始值。这个函数是 `const fn`，这意味着它可以在编译时使用。

*   **`load(&self, order: Ordering) -> u64`:**  以指定的 `Ordering` 加载原子值。实际上，它获取 `Mutex` 的锁，读取值，然后释放锁。

*   **`fetch_add(&self, val: u64, order: Ordering) -> u64`:**  原子地将 `val` 加到当前值上，并返回旧值。它获取锁，执行加法，然后释放锁。

*   **`compare_exchange_weak(&self, current: u64, new: u64, _success: Ordering, _failure: Ordering) -> Result<u64, u64>`:**  尝试原子地将当前值与 `current` 比较，如果相等，则将值设置为 `new`。它获取锁，执行比较和交换，然后释放锁。由于使用了 `Mutex`，所以这个操作不是弱的，它总是成功或失败。

*   **`inner(&self) -> &Mutex<u64>`:**  这是一个私有方法，用于获取 `Mutex` 的引用。它使用 `OnceCell` 来确保 `Mutex` 只被创建一次，并使用 `init` 值进行初始化。

**如何融入项目：**

这个文件提供了在编译时初始化原子变量的能力，这对于需要静态原子变量的场景非常有用。它使用 `Mutex` 和 `OnceCell` 来确保线程安全和延迟初始化。它模拟了原子操作，但实际上是通过互斥锁来实现的，这在 loom 的上下文中是可接受的，因为 loom 主要用于测试并发代码。
