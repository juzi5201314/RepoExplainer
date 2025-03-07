# 代码文件解释：`task.rs`

## 目的
该文件提供了基于 Tokio 的异步测试工具，核心是 `Spawn` 结构体。它通过模拟任务执行环境，简化了手动驱动 `Future` 和 `Stream` 的测试流程。主要功能包括：
1. 自动处理 `Future` 的 `Pin` 和 `Context` 等复杂性
2. 跟踪任务被唤醒的次数，验证任务间通知的正确性
3. 支持直接测试需要 Tokio 上下文的异步代码

## 核心组件

### 1. `Spawn` 结构体
```rust
pub struct Spawn<T> {
    task: MockTask,
    future: Pin<Box<T>>,
}
```
- **功能**：包装任意 `Future` 或 `Stream`，提供简化接口进行手动轮询
- **关键方法**：
  - `poll()`：自动处理 `Future` 的 `poll`
  - `poll_next()`：自动处理 `Stream` 的 `poll_next`
  - `is_woken()`：检查自上次轮询后是否被唤醒
  - `enter()`：在任务上下文中执行闭包，管理 `Context` 和唤醒状态

### 2. `MockTask` 模拟任务
```rust
struct MockTask {
    waker: Arc<ThreadWaker>,
}
```
- **功能**：模拟 Tokio 任务运行时环境
- **核心机制**：
  - 使用 `ThreadWaker` 跟踪唤醒状态（`IDLE`, `WAKE`, `SLEEP`）
  - 通过 `RawWaker` 实现自定义唤醒逻辑
  - `enter()` 方法创建安全的 `Context` 环境

### 3. `ThreadWaker` 唤醒管理器
```rust
struct ThreadWaker {
    state: Mutex<usize>,
    condvar: Condvar,
}
```
- **功能**：管理任务的唤醒状态和通知机制
- **关键操作**：
  - `wake()`：改变状态并通知等待线程
  - `clear()`：重置唤醒状态（在每次轮询前调用）
  - 使用 `Mutex` 和 `Condvar` 实现线程安全的状态同步

### 4. 原始唤醒函数
```rust
static VTABLE: RawWakerVTable = RawWakerVTable::new(clone, wake, wake_by_ref, drop_waker);
```
- 实现 `RawWaker` 接口：
  - `clone()`：增加引用计数
  - `wake()`：触发任务唤醒
  - `drop_waker()`：释放资源

## 工作流程
1. **创建测试任务**：通过 `task::spawn(fut)` 将 `Future` 包装为 `Spawn`
2. **手动轮询**：调用 `task.poll()` 或 `task.poll_next()` 驱动异步操作
3. **状态检查**：通过 `task.is_woken()` 验证任务是否被正确唤醒
4. **上下文管理**：`enter()` 方法自动处理 `Context` 创建和状态重置

## 在项目中的角色