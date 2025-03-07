# `WakeList` 模块详解

## 概述  
`WakeList` 是 Tokio 内部用于批量管理 `Waker` 对象的实用工具，主要负责高效地收集和唤醒多个等待任务的唤醒器。该模块通过固定大小的数组（容量为 32）实现内存优化，并确保线程安全和资源正确释放。

---

## 核心结构

### `WakeList` 结构体
```rust
pub(crate) struct WakeList {
    inner: [MaybeUninit<Waker>; NUM_WAKERS],
    curr: usize,
}
```
- **`inner`**: 使用 `MaybeUninit<Waker>` 数组存储未初始化的 `Waker` 对象，容量固定为 `NUM_WAKERS`（32）。
- **`curr`**: 记录当前已存储的 `Waker` 数量，确保 `inner` 的前 `curr` 个元素是已初始化的。

#### 不变式（Invariant）
- `inner` 的前 `curr` 个元素始终是有效初始化的 `Waker`。

---

## 核心方法

### 初始化与容量检查
```rust
pub(crate) fn new() -> Self { ... }
pub(crate) fn can_push(&self) -> bool { ... }
```
- **`new()`**: 创建空的 `WakeList`，所有元素初始化为未初始化状态。
- **`can_push()`**: 检查是否还能添加新的 `Waker`（`curr < 32`）。

### 添加与唤醒操作
```rust
pub(crate) fn push(&mut self, val: Waker) { ... }
pub(crate) fn wake_all(&mut self) { ... }
```
- **`push()`**: 将 `Waker` 添加到数组末尾，需确保容量未满。
- **`wake_all()`**: 批量唤醒所有存储的 `Waker`，关键逻辑如下：
  1. 使用 `DropGuard` 结构体管理内存安全：
     - `DropGuard` 通过 `start` 和 `end` 指针跟踪待唤醒的 `Waker` 范围。
     - 若中途发生 panic，`DropGuard` 的 `Drop` 实现会安全释放剩余资源。
  2. 循环遍历所有 `Waker`，逐个调用 `.wake()`。
  3. 完成后重置 `curr` 为 0，避免重复唤醒。

### 内存释放
```rust
impl Drop for WakeList {
    fn drop(&mut self) { ... }
}
```
- 在 `WakeList` 被销毁时，确保未被唤醒的 `Waker` 被正确释放，避免内存泄漏。

---

## 设计亮点
1. **固定容量优化**：通过预分配 `MaybeUninit<Waker>` 数组，避免动态内存分配开销。
2. **批量唤醒机制**：将多次独立唤醒操作合并为一次批量处理，减少系统调用次数。
3. **安全内存管理**：
   - 使用 `MaybeUninit` 避免未使用的空间被错误初始化。
   - `DropGuard` 确保 panic 时资源正确释放。
   - 显式 `Drop` 实现保证未处理的 `Waker` 被清理。

---

## 在项目中的角色
`WakeList` 是 Tokio 异步运行时的核心组件之一，用于高效管理 I/O 或任务等待时的唤醒操作，通过批量处理提升性能并确保内存安全。它常被用于事件循环中，收集等待任务的 `Waker` 并在事件触发时统一唤醒，是异步编程中优化并发性能的关键工具。
