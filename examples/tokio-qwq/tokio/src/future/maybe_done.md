# `tokio/src/future/maybe_done.rs` 文件详解

## 文件目的
该文件定义了 Tokio 异步运行时中的 `MaybeDone` 组合子（combinator），用于跟踪一个异步任务（Future）的完成状态。它允许在不立即消耗 Future 的情况下，安全地检查或获取已完成任务的结果。

---

## 核心组件

### 1. `MaybeDone` 枚举
```rust
pub enum MaybeDone<Fut: Future> {
    Future { #[pin] future: Fut }, // 未完成的 Future
    Done { output: Fut::Output },  // 已完成的 Future 及其结果
    Gone,                         // 已通过 take_output() 取出结果后的空状态
}
```
- **状态管理**：
  - `Future`：包含未完成的异步任务。
  - `Done`：存储已完成任务的输出结果。
  - `Gone`：表示结果已被 `take_output()` 方法取出，后续操作会触发 panic。

### 2. `maybe_done` 工厂函数
```rust
pub fn maybe_done<F: IntoFuture>(future: F) -> MaybeDone<F::IntoFuture> { ... }
```
将任意 `IntoFuture` 类型包装为 `MaybeDone`，初始化为 `Future` 状态。

---

## 核心方法

### 1. `output_mut()`
```rust
pub fn output_mut(self: Pin<&mut Self>) -> Option<&mut Fut::Output> {
    match self.project() {
        MaybeDoneProj::Done { output } => Some(output),
        _ => None,
    }
}
```
- **功能**：返回已完成任务的可变引用（仅在 `Done` 状态且未调用 `take_output()` 时有效）。

### 2. `take_output()`
```rust
pub fn take_output(self: Pin<&mut Self>) -> Option<Fut::Output> { ... }
```
- **功能**：取出已完成任务的结果，将状态转为 `Gone`，后续无法再次获取结果。

### 3. `Future` 实现的 `poll()` 方法
```rust
fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
    match self.as_mut().project() {
        MaybeDoneProj::Future { future } => {
            let output = ready!(future.poll(cx));
            self.set(MaybeDone::Done { output });
            Poll::Ready(())
        },
        MaybeDoneProj::Done { .. } => Poll::Ready(()),
        MaybeDoneProj::Gone => panic!("..."),
    }
}
```
- **行为**：
  - 若处于 `Future` 状态，驱动内部 Future 执行。
  - 当 Future 完成后，将状态转为 `Done` 并返回结果。
  - 已完成或 `Gone` 状态时直接返回 `Poll::Ready`。

---

## 作用与项目集成
该文件通过 `MaybeDone` 组合子实现了以下功能：
1. **状态追踪**：明确区分 Future 的未完成、已完成、已取结果三种状态。
2. **安全访问**：允许在不提前消耗 Future 的情况下，安全地检查或获取结果。
3. **生命周期管理**：通过 `Gone` 状态防止重复访问已取出的结果。

### 在项目中的角色
作为 Tokio 异步编程框架的核心组件之一，`MaybeDone` 提供了对异步任务完成状态的精细控制，支持在复杂异步流程中安全地管理和复用 Future 的结果，是构建高级异步组合子的重要基础。
