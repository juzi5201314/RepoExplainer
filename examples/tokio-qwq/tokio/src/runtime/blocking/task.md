# 文件说明：`tokio/src/runtime/blocking/task.rs`

## 文件目的
该文件定义了 Tokio 运行时中用于执行阻塞任务的核心结构 `BlockingTask`，将同步函数转换为异步 Future，使其能够在异步运行时中安全执行阻塞操作。

---

## 关键组件

### 1. `BlockingTask<T>` 结构体
```rust
pub(crate) struct BlockingTask<T> {
    func: Option<T>,
}
```
- **功能**：包装一个闭包或函数，将其转换为 Future。
- **字段**：
  - `func`: 使用 `Option<T>` 存储待执行的函数，执行后置为 `None` 以防止重复调用。

### 2. `new` 方法
```rust
pub(crate) fn new(func: T) -> BlockingTask<T> {
    BlockingTask { func: Some(func) }
}
```
- **作用**：初始化 `BlockingTask`，将传入的函数安全地包装到 `func` 字段中。

### 3. `Unpin` 实现
```rust
impl<T> Unpin for BlockingTask<T> {}
```
- **目的**：标记该结构体不需要 Pin 机制，允许在堆上自由移动而不影响执行。

### 4. `Future` 特性实现
```rust
impl<T, R> Future for BlockingTask<T>
where
    T: FnOnce() -> R + Send + 'static,
    R: Send + 'static,
{
    type Output = R;

    fn poll(...) -> Poll<R> { ... }
}
```
- **关键逻辑**：
  - **执行函数**：通过 `func.take()` 取出闭包并执行，确保只执行一次。
  - **调度控制**：调用 `crate::task::coop::stop()` 禁用协作调度（Cooperative Scheduling），避免阻塞任务被时间片机制中断。
  - **返回结果**：直接返回 `Poll::Ready(func())`，表示 Future 已完成。

---

## 工作原理
1. **转换为 Future**：通过 `BlockingTask::new` 将同步函数包装为 Future。
2. **调度隔离**：执行前禁用协作调度，确保阻塞任务不会被提前中断。
3. **单次执行**：通过 `Option<T>` 确保函数仅执行一次，防止重复调用。
4. **无缝集成**：作为 Future 可被 Tokio 运行时轮询，支持在异步上下文中执行阻塞操作。

---

## 在项目中的角色
该文件为 Tokio 运行时提供了阻塞任务的执行核心，通过将同步代码转换为 Future，实现了阻塞操作与异步生态系统的安全集成，确保运行时在处理长时间任务时仍能保持高效调度。

```rust
// 最后一行：简要描述文件角色