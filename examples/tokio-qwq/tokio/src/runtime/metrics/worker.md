# 文件说明：`tokio/src/runtime/metrics/worker.rs`

## **功能与目的**  
该文件定义了 Tokio 运行时中 **Worker 线程的性能指标结构体 `WorkerMetrics`**，用于收集和跟踪工作线程在任务调度、执行和资源使用方面的关键数据。这些指标帮助开发者监控运行时性能、调试线程行为，并优化任务调度策略。

---

## **核心组件与字段说明**

### **1. 结构体 `WorkerMetrics`**
```rust
pub(crate) struct WorkerMetrics { ... }
```
- **字段类型**：所有计数器字段均为原子类型（`MetricAtomicU64` 或 `MetricAtomicUsize`），确保多线程安全访问。
- **关键字段**：
  - **基础计数器**：
    - `park_count`: 线程因无任务而进入等待状态的次数。
    - `park_unpark_count`: 线程被唤醒后立即再次进入等待的次数。
    - `noop_count`: 线程唤醒后未执行任务便再次等待的次数。
    - `steal_count`: 从其他线程窃取任务的总数。
    - `poll_count`: 线程主动执行任务的次数。
    - `busy_duration_total`: 线程处于活跃状态（非等待）的总时间（纳秒）。
  - **队列相关**：
    - `local_schedule_count`: 本地队列调度任务的次数。
    - `overflow_count`: 因本地队列满而溢出到全局队列的任务数。
    - `queue_depth`: 当前线程本地队列的任务数量（仅适用于单线程调度器）。
  - **性能统计**：
    - `mean_poll_time`: 任务执行时间的指数加权移动平均值（EWMA）。
    - `poll_count_histogram`: 可选的执行时间分布直方图（`Histogram` 类型）。
  - **线程标识**：
    - `thread_id`: 线程的唯一标识（通过 `Mutex<Option<ThreadId>>` 存储）。

### **2. 方法与初始化**
- **`from_config`**：根据配置初始化 `WorkerMetrics`，若配置中启用了 `poll_count_histogram`，则构建对应的直方图。
- **`queue_depth`/`set_queue_depth`**：获取或设置本地队列的当前深度。
- **`thread_id`/`set_thread_id`**：通过互斥锁安全地获取或设置线程 ID。

---

## **实现细节**
- **内存对齐**：`#[repr(align(128))]` 确保结构体在内存中按 128 字节对齐，减少伪共享（False Sharing）对性能的影响。
- **原子操作**：所有计数器字段使用原子类型，避免多线程竞争条件。
- **可选直方图**：`poll_count_histogram` 允许按需启用更细粒度的执行时间统计。

---

## **项目中的角色**
该文件是 Tokio 运行时 **指标收集系统** 的核心组件之一，负责记录工作线程的运行状态和性能数据。它与其他模块（如调度器、全局指标聚合器）协作，为用户提供运行时性能分析和诊断能力。通过这些指标，开发者可以优化任务分配策略、识别性能瓶颈，并确保多线程任务调度的高效性。

**文件在项目中的角色**：  