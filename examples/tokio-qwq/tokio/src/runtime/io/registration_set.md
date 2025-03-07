# 文件说明：`registration_set.rs`

## 文件目的
该文件实现了 Tokio 运行时中 I/O 资源注册与释放的管理机制。通过 `RegistrationSet` 和 `Synced` 结构体，协调 I/O 资源的生命周期管理，确保资源注册、注销和清理过程的安全性与高效性。

---

## 核心组件

### 1. `RegistrationSet`
- **功能**：管理 I/O 资源的注册与释放逻辑，提供线程安全的操作接口。
- **关键字段**：
  - `num_pending_release`: 使用 `AtomicUsize` 跟踪待释放的 I/O 资源数量，确保跨线程可见性。
- **关键方法**：
  - `allocate()`: 创建新的 `ScheduledIo` 实例并加入活跃列表。
  - `deregister()`: 将废弃的 `ScheduledIo` 移至待释放队列，并判断是否需通知驱动程序处理。
  - `release()`: 批量处理待释放的资源，确保安全移除。
  - `shutdown()`: 标记运行时关闭状态，回收所有未处理的 I/O 资源。

### 2. `Synced`
- **功能**：存储共享状态，需通过原子操作或锁访问。
- **关键字段**：
  - `registrations`: 使用 `LinkedList` 存储所有活跃的 `ScheduledIo`。
  - `pending_release`: 存储待释放的 `ScheduledIo`，容量阈值为 `NOTIFY_AFTER`（默认 16）。
  - `is_shutdown`: 标记 I/O 驱动是否已关闭。

### 3. 辅助结构
- **`LinkedList<Arc<ScheduledIo>, ScheduledIo>`**: 自定义链表实现，用于高效管理活跃 I/O 资源。
- **`unsafe impl Link for Arc<ScheduledIo>`**: 通过不安全代码实现链表节点操作，依赖 `Arc` 的内存安全保证。

---

## 核心逻辑流程

### 资源注册流程
1. 调用 `allocate()` 创建新 `ScheduledIo`。
2. 将其加入 `registrations` 链表头部。
3. 返回资源句柄供外部使用。

### 资源释放流程
1. 调用 `deregister()` 将废弃资源加入 `pending_release`。
2. 当 `pending_release` 达到阈值 `NOTIFY_AFTER`，通知驱动程序处理。
3. 驱动调用 `release()` 批量移除资源：
   - 从 `registrations` 中安全删除节点。
   - 重置计数器。

### 关闭流程
1. 调用 `shutdown()` 标记运行时关闭。
2. 清空 `pending_release`。
3. 回收所有活跃资源（遍历 `registrations` 列表）。

---

## 线程安全机制
- **原子操作**：`num_pending_release` 使用 `AtomicUsize` 确保跨线程计数安全。
- **内存屏障**：`Acquire` 和 `Release` 语义保证操作的可见性与顺序。
- **不安全代码**：通过 `unsafe` 块操作原始指针，依赖 `Arc` 的内存管理保证安全性。

---

## 在项目中的角色
该文件是 Tokio 运行时 I/O 子系统的核心组件，负责管理 I/O 资源的注册、释放和生命周期，确保多线程环境下的资源安全与高效回收，是 I/O 驱动与任务调度协同工作的关键基础设施。
