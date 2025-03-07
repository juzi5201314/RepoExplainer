# CancellationToken.rs 文件详解

## 功能概述
该文件实现了 Tokio 生态中的 `CancellationToken` 结构体，用于在异步任务间传递取消请求信号。通过该结构体，任务可以等待取消事件（通过 `cancelled()` 方法返回的 Future），并支持通过 `cancel()` 方法主动触发取消操作。

---

## 核心组件

### 1. CancellationToken 结构体
```rust
pub struct CancellationToken {
    inner: Arc<TreeNode>,
}
```
- **TreeNode 内部结构**：通过 `Arc<TreeNode>` 管理共享状态，支持多线程安全的引用计数和取消状态跟踪。
- **关键方法**：
  - `new()`：创建未取消的初始状态。
  - `child_token()`：创建子令牌，父令牌取消时会级联通知子令牌，但子令牌取消不会影响父令牌。
  - `cancel()`：标记为已取消并唤醒所有等待任务。
  - `is_cancelled()`：检查当前是否已取消。

### 2. 取消等待 Future
#### a. 引用式 Future
```rust
pub struct WaitForCancellationFuture<'a> {
    cancellation_token: &'a CancellationToken,
    #[pin] future: Notified<'a>,
}
```
- 通过 `cancellation_token.cancelled()` 获得，依赖对 `CancellationToken` 的引用。
- 内部使用 Tokio 的 `Notified` Future 监听取消事件。

#### b. 所有权式 Future
```rust
pub struct WaitForCancellationFutureOwned {
    #[pin] future: MaybeDangling<Notified<'static>>,
    cancellation_token: CancellationToken,
}
```
- 通过 `cancellation_token.cancelled_owned()` 获得，完全拥有令牌所有权。
- 使用 `MaybeDangling` 确保 Future 的生命周期不超过令牌，避免悬垂指针问题。

### 3. 安全性保障
- **Cancel Safety**：所有取消操作保证线程安全，Future 的 `poll` 方法在取消后立即返回。
- **引用计数管理**：通过 `TreeNode` 的 `increase_handle_refcount` 和 `decrease_handle_refcount` 方法维护引用计数，确保资源正确释放。

---

## 核心逻辑流程
1. **创建与克隆**：
   - `CancellationToken::new()` 初始化根节点。
   - `clone()` 方法增加引用计数，共享同一 `TreeNode`。
   - `child_token()` 创建子节点，形成层级结构。

2. **取消触发**：
   - 调用 `cancel()` 标记节点为已取消，并唤醒所有监听的 Future。
   - 取消操作会级联通知所有子节点。

3. **等待取消**：
   - `WaitForCancellationFuture` 通过 `poll` 方法轮询 `Notified`，直到检测到取消状态。
   - 若令牌已提前取消，Future 立即返回 `Poll::Ready`。

4. **集成示例**：
   ```rust
   let token = CancellationToken::new();
   let cloned_token = token.clone();
   // 在任务中等待取消或超时
   select! {
       _ = cloned_token.cancelled() => { /* 取消处理 */ }
       _ = sleep(Duration::from_secs(9999)) => { /* 超时处理 */ }
   }
   ```

---

## 项目中的角色
该文件是 Tokio 异步取消机制的核心实现，提供安全、高效的取消信号传递能力，支持任务间协作中断，是构建可靠异步程序的重要基础组件。
