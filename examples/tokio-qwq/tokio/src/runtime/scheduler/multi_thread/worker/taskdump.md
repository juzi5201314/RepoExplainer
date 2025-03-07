# 文件解释：`taskdump.rs`

## 文件目的
该文件实现了 Tokio 多线程调度器中任务转储（Task Dump）的核心逻辑，用于在运行时收集所有任务的执行状态信息。这一功能主要用于调试和性能分析，帮助开发者快速定位任务阻塞或死锁等问题。

---

## 关键组件与功能

### 1. `Handle::trace_core` 方法
#### 核心逻辑：
- **线程协调**：
  - 使用 `trace_status` 的屏障机制同步所有工作线程，确保只有一个线程（leader）执行实际的追踪操作。
  - 设置 250ms 超时机制，若超时则放弃追踪。
  - 非 leader 线程等待 leader 完成追踪后直接返回。
- **任务收集**：
  - 调用 `Shared::steal_all()` 将所有远程队列的任务集中到本地队列。
- **任务追踪**：
  - 调用 `trace_multi_thread` 安全地遍历所有任务，生成任务追踪数据。
  - 将追踪结果转换为 `dump::Task` 格式并存储到共享状态中。
- **线程释放**：
  - 通过 `trace_end` 通知其他线程追踪完成，解除等待。

#### 关键代码片段：
```rust
// 线程屏障同步
let barrier = if let Some(barrier) = self.shared.trace_status.trace_start.wait_timeout(timeout) {
    barrier
} else {
    return core;
};

// 任务追踪与结果存储
let traces = unsafe { trace_multi_thread(...) }
    .into_iter()
    .map(|(id, trace)| dump::Task::new(id, trace))
    .collect();
self.shared.trace_status.stash_result(dump::Dump::new(traces));
```

---

### 2. `Shared::steal_all` 方法
#### 功能：
从所有远程任务队列中窃取任务，集中到本地队列中，确保追踪时能捕获所有任务状态。

#### 实现细节：
- 遍历 `self.remotes` 中的每个远程队列。
- 使用 `steal_into` 方法将远程任务转移到本地队列 `local`。
- 统计窃取任务的性能指标（通过 `Stats` 结构）。

#### 关键代码片段：
```rust
for remote in self.remotes.iter() {
    while !steal.is_empty() {
        if let Some(task) = steal.steal_into(&mut local, &mut stats) {
            local.push_back([task].into_iter());
        }
    }
}
```

---

## 与其他模块的交互
- **依赖模块**：
  - `trace_multi_thread`：底层任务遍历函数（需 `unsafe` 调用，确保线程安全）。
  - `dump`：任务转储数据结构，负责将追踪结果格式化。
  - `WorkerMetrics` 和 `Stats`：记录任务窃取和调度的统计信息。
- **调用场景**：
  - 当用户调用 `runtime.dump()` 时触发，通过 `Handle` 协调多线程环境下的任务状态收集。

---

## 在项目中的角色