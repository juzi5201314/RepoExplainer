# `batch.rs` 文件详解

## **文件目的**
该文件定义了 Tokio 运行时中用于收集和批量提交线程工作者（Worker）运行指标的核心结构 `MetricsBatch`。通过批量处理指标更新，减少频繁的原子操作开销，同时提供细粒度的性能监控数据，帮助分析任务调度、任务窃取、任务执行时间等关键行为。

---

## **关键组件**

### **1. `MetricsBatch` 结构**
#### **字段说明**
- **基础计数器**：
  - `park_count`: 工作者主动进入休眠的次数。
  - `park_unpark_count`: 休眠后被唤醒的次数（反映线程调度活跃度）。
  - `noop_count`: 休眠后未执行任务即被唤醒的次数（空唤醒）。
  - `steal_count`: 成功窃取其他工作者任务的总数。
  - `poll_count`: 工作者主动轮询任务的次数。
  - `local_schedule_count`: 本地队列成功调度任务的次数。
  - `overflow_count`: 因本地队列满而将任务转移到全局队列的次数。

- **时间相关指标**：
  - `busy_duration_total`: 工作者处于活跃状态（非休眠）的总时长（纳秒）。
  - `processing_scheduled_tasks_started_at`: 最近一次处理任务批次的起始时间戳。

- **细粒度跟踪**：
  - `poll_timer`: 使用 `HistogramBatch` 统计单次任务轮询耗时的直方图数据。

#### **方法功能**
- **初始化**：
  `new()` 初始化所有计数器，并记录当前时间戳，为 `poll_timer` 配置直方图支持。

- **指标更新**：
  - `about_to_park()`: 记录休眠前的指标，判断是否为空唤醒。
  - `unparked()`: 更新唤醒计数。
  - `start_poll()` / `end_poll()`: 跟踪单次任务轮询的耗时。
  - `start_processing_scheduled_tasks()` / `end_processing_scheduled_tasks()`: 统计任务批次处理的活跃时长。

- **批量提交**：
  `submit()` 将批量收集的指标原子地写入 `WorkerMetrics`，确保线程安全。

### **2. `PollTimer` 结构**
嵌套结构，用于记录单次任务轮询的耗时分布：
- `poll_counts`: 直方图数据，按时间区间统计轮询耗时。
- `poll_started_at`: 最近一次轮询的起始时间戳。

### **3. 辅助函数**
- `duration_as_u64()`: 将 `Duration` 转换为纳秒级 `u64`，溢出时返回最大值。

---

## **多线程扩展**
通过 `cfg_rt_multi_thread!` 宏为多线程场景添加额外方法：
- `incr_steal_count()` / `incr_steal_operations()`: 更新任务窃取相关指标。
- `incr_overflow_count()`: 记录本地队列溢出次数。

---

## **与项目其他部分的交互**
1. **数据来源**：
   - `WorkerMetrics`（来自 `crate::runtime::metrics`）是共享的原子指标容器，`MetricsBatch` 通过 `submit()` 将批量数据提交至此。
   - `HistogramBatch` 用于聚合任务轮询时间的分布数据，支持后续生成直方图。

2. **使用场景**：
   - 在工作者线程循环中，通过调用 `MetricsBatch` 的方法（如 `start_poll()`、`about_to_park()`）实时记录操作。
   - 定期调用 `submit()` 将数据同步到全局指标，供监控或日志模块读取。

3. **性能优化**：
   - 批量更新机制减少原子操作频率，降低性能开销。
   - 直方图统计通过 `HistogramBatch` 实现高效时间区间划分。

---

## **文件在项目中的角色**