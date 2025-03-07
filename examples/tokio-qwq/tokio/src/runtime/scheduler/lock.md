# 文件说明：`lock.rs`

## 目的
该文件定义了 Tokio 运行时调度器中使用的锁（Mutex）抽象和具体实现。通过封装标准库的 `sync::Mutex`，提供了符合异步运行时需求的锁机制，支持资源安全共享和高效的线程调度。

---

## 核心组件

### 1. **`Lock` 特征（Trait）**
```rust
pub(crate) trait Lock<T> {
    type Handle: AsMut<T>;
    fn lock(self) -> Self::Handle;
}
```
- **作用**：定义锁的基本行为，要求实现者提供一种获取锁的句柄（Handle）的方式。
- **关键点**：
  - `Handle` 必须实现 `AsMut<T>`，确保获取到的资源可以安全地进行可变访问。
  - `lock()` 方法返回锁的句柄，用于访问被保护的数据。

---

### 2. **`Mutex` 结构体**
```rust
pub(crate) struct Mutex<T: ?Sized>(sync::Mutex<T>);
```
- **作用**：封装标准库的 `sync::Mutex`，提供 Tokio 专用的锁实现。
- **关键方法**：
  - **`const_new` 和 `new`**：
    ```rust
    pub(crate) const fn const_new(t: T) -> Mutex<T> { ... }
    pub(crate) fn new(t: T) -> Mutex<T> { ... }
    ```
    初始化新 `Mutex` 实例，支持常量初始化和普通初始化。

  - **`lock` 方法**：
    ```rust
    pub(crate) fn lock(&self) -> MutexGuard<'_, T> { ... }
    ```
    - 安全获取锁的 guard，处理锁的“中毒”（Poisoning）状态：
      - 第一种实现直接调用 `unwrap()`，可能 panic。
      - 第二种实现通过 `Err(p_err).into_inner()` 回收中毒的 guard，避免传播 panic。

  - **`try_lock` 方法**：
    ```rust
    pub(crate) fn try_lock(&self) -> Option<MutexGuard<'_, T>> { ... }
    ```
    尝试无阻塞获取锁，失败时返回 `None`。

  - **`wait` 方法**：
    ```rust
    pub(crate) fn wait<'a, T>(&self, mut guard: MutexGuard<'a, T>) -> LockResult<MutexGuard<'a, T>> { ... }
    ```
    在持有锁时等待通知，用于异步任务的协作调度（如等待 I/O 完成后唤醒任务）。

---

### 3. **`MutexGuard` 守护结构体**
- **作用**：锁的持有凭证，实现 `AsMut<T>`，确保安全访问内部数据。
- **生命周期管理**：自动释放锁，避免死锁。

---

## 与项目的关系
此文件是 Tokio 运行时调度器的核心组件之一，提供以下功能：
1. **资源安全共享**：通过锁机制保护共享数据，避免竞态条件。
2. **异步友好**：`wait` 方法与 Tokio 的任务调度器协作，实现高效的线程切换。
3. **错误处理**：优雅处理锁的中毒状态，避免因单个任务 panic 导致全局不可用。

### 文件角色