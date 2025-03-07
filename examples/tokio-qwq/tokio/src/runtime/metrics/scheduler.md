# `scheduler.rs` 文件详解

## **文件目的**  
该文件定义了 Tokio 运行时调度器的指标统计结构 `SchedulerMetrics`，用于收集与任务调度相关的运行时内部数据。这些指标帮助开发者监控调度行为，优化性能，并诊断潜在的资源竞争或任务饥饿问题。

---

## **关键组件**

### **1. `SchedulerMetrics` 结构体**
```rust
pub(crate) struct SchedulerMetrics {
    pub(super) remote_schedule_count: MetricAtomicU64,
    pub(super) budget_forced_yield_count: MetricAtomicU64,
}
```
- **字段说明**：
  - **`remote_schedule_count`**：记录从运行时外部（如通过 `tokio::task::spawn`）调度的任务数量。  
  - **`budget_forced_yield_count`**：记录因任务耗尽时间预算（budget）而被迫让出执行权的次数。这与 Tokio 的**协作式调度**机制相关，防止任务独占 CPU 导致饥饿。

- **`MetricAtomicU64` 类型**：基于原子操作的无符号 64 位整数，确保多线程环境下的安全计数。

### **2. 方法实现**
#### **初始化方法**
```rust
pub(crate) fn new() -> SchedulerMetrics {
    SchedulerMetrics {
        remote_schedule_count: MetricAtomicU64::new(0),
        budget_forced_yield_count: MetricAtomicU64::new(0),
    }
}
```
初始化两个计数器为 `0`。

#### **计数器递增方法**
```rust
pub(crate) fn inc_remote_schedule_count(&self) {
    self.remote_schedule_count.add(1, Relaxed);
}

pub(crate) fn inc_budget_forced_yield_count(&self) {
    self.budget_forced_yield_count.add(1, Relaxed);
}
```
- **`add(1, Relaxed)`**：使用原子操作递增计数器，`Relaxed` 表示不强制内存顺序，保证高效性。
- **作用**：分别记录外部调度任务和强制让步事件的发生次数。

---

## **与项目其他部分的关联**
1. **WorkerMetrics 和多线程调度**  
   在相关代码中，`SchedulerMetrics` 通过 `scheduler_metrics()` 方法暴露给更高层的 `WorkerMetrics`（工作线程指标结构），表明其是 Tokio 多线程调度器整体监控的一部分。

2. **协作式调度机制**  
   文件注释提到“**协作式调度（coop）**”机制，`budget_forced_yield_count` 直接关联此机制：当任务耗尽时间预算时，调度器强制其让出执行权，避免单任务长时间独占 CPU。

3. **不稳定性声明**  
   文件顶部的 **`unstable API`** 警告表明，此接口可能在 Tokio 1.x 版本中变更，开发者需谨慎依赖。

---

## **文件在项目中的角色**  
该文件是 Tokio 运行时**指标收集系统**的核心组件之一，通过原子计数器统计调度器的关键行为（如外部任务调度和强制让步），为运行时性能分析、调试和优化提供数据支持。它帮助开发者理解任务调度模式，识别潜在的资源竞争或饥饿问题。  

最后描述：  