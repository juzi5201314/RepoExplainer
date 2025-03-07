### 代码文件解释：`task_tracker.rs`

#### 目的
`TaskTracker` 是 Tokio 生态系统中用于跟踪异步任务并实现优雅关闭的工具。它允许开发者在任务完成时立即释放内存，并通过 `close` 和 `wait` 方法控制任务集合的关闭流程，特别适用于需要协调多个任务有序终止的场景。

#### 核心组件
1. **`TaskTracker` 结构体**
   - **内部状态 (`TaskTrackerInner`)**:
     - `state`: 使用 `AtomicUsize` 存储任务计数和关闭标志。最低位表示是否关闭，其余位表示当前活跃任务数量。
     - `on_last_exit`: 使用 `Notify` 实现等待任务完成时的异步通知。
   - **方法**:
     - `new()`: 创建新实例，默认处于打开状态。
     - `close()` / `reopen()`: 控制任务集合的关闭状态。
     - `wait()`: 返回一个 Future，等待任务集合关闭且所有任务完成。
     - `spawn` 系列方法: 将任务提交到 Tokio 运行时并自动跟踪。
     - `track_future()`: 将任意 Future 转换为 `TrackedFuture`，确保任务被跟踪。

2. **`TaskTrackerToken`**
   - 表示被跟踪的任务。当 `Token` 被丢弃时，任务计数减少，表示任务完成。

3. **`TrackedFuture`**
   - 包装用户提供的 Future，通过持有 `TaskTrackerToken` 确保任务被跟踪，直到 Future 完成或被丢弃。

4. **`TaskTrackerWaitFuture`**
   - 由 `TaskTracker::wait()` 返回的 Future，负责等待任务集合关闭且所有任务完成。通过原子操作和 `Notify` 实现高效等待。

#### 关键特性
- **内存优化**: 任务完成时立即从跟踪器中移除，避免内存泄漏（与 `JoinSet` 不同，后者保留任务结果）。
- **关闭控制**: 需要显式调用 `close()` 后，`wait()` 才会返回，即使任务已全部完成。
- **可扩展性**: 支持克隆 `TaskTracker` 实例，方便在多个任务间共享跟踪逻辑。

#### 与其他组件的对比
- **与 `JoinSet` 的区别**:
  - `TaskTracker` 不存储任务结果，任务完成即释放资源。
  - 允许在任务集合为空但未关闭时继续添加新任务。
  - 无需可变引用即可添加任务，更易共享。

#### 使用场景示例
```rust
// 示例：优雅关闭任务
let tracker = TaskTracker::new();
let token = CancellationToken::new();

// 启动任务并跟踪
for i in 0..10 {
    tracker.spawn(async move {
        // 使用 CancellationToken 实现任务终止
        tokio::select! {
            _ = background_task() => {},
            _ = token.cancelled() => { /* 清理 */ }
        }
    });
}

// 关闭跟踪器并触发取消
tracker.close();
token.cancel();
tracker.wait().await; // 等待所有任务完成
```

#### 在项目中的角色