# 文件说明：`explanations/tokio/tokio/src/runtime/scheduler/multi_thread/stats.rs`

## **文件目的**
该文件定义了 Tokio 运行时多线程调度器中用于统计和调优的核心结构 `Stats`。其主要作用是收集每个工作线程（Worker）的运行时指标，用于动态调整调度策略（如全局队列检查频率），并为用户提供运行时统计信息。

---

## **关键组件与功能**

### **1. `Stats` 结构体**
#### **字段说明**
- **`batch: MetricsBatch`**  
  聚合运行时指标的批次对象，负责将统计结果提交给 `WorkerMetrics`。未来计划与 `Stats` 合并（当指标功能稳定后）。
  
- **`processing_scheduled_tasks_started_at: Instant`**  
  记录当前批次任务开始处理的时间点，用于计算任务处理耗时。

- **`tasks_polled_in_batch: usize`**  
  当前批次中已轮询的任务数量计数器。

- **`task_poll_time_ewma: f64`**  
  任务轮询时间的指数加权移动平均值（EWMA），以纳秒为单位存储为浮点数，用于动态调整调度策略。

#### **常量定义**
- **`TASK_POLL_TIME_EWMA_ALPHA`**  
  EWMA 的衰减系数（0.1），控制历史数据与新数据的权重比例。

- **`TARGET_GLOBAL_QUEUE_INTERVAL`**  
  目标全局队列检查间隔（200 微秒），用于计算默认的任务轮询次数。

- **`MAX_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`**  
  全局队列检查间隔内允许的最大任务轮询次数（127），防止过度轮询。

- **`TARGET_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`**  
  默认目标任务轮询次数（61），用于初始化 EWMA。

---

### **2. 核心方法**
#### **`new()` 初始化方法**
- **功能**：初始化 `Stats` 实例。
- **关键操作**：
  - 使用 `TARGET_GLOBAL_QUEUE_INTERVAL / TARGET_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL` 初始化 `task_poll_time_ewma`，作为初始 EWMA 值。

#### **`tuned_global_queue_interval()` 动态调整方法**
- **功能**：根据当前 EWMA 计算全局队列检查间隔。
- **逻辑**：
  - 若配置中已显式设置间隔值，则直接返回。
  - 否则，通过 `TARGET_GLOBAL_QUEUE_INTERVAL / task_poll_time_ewma` 计算任务轮询次数，并限制在 `[2, 127]` 范围内。

#### **`start_processing_scheduled_tasks()` 和 `end_processing_scheduled_tasks()`**
- **功能**：开始/结束处理任务批次时的统计操作。
- **关键操作**：
  - `start`：记录开始时间并重置计数器。
  - `end`：计算当前批次的平均任务轮询时间，并更新 EWMA：
    ```rust
    mean_poll_duration = 总耗时 / 任务数
    weighted_alpha = 1 - (1 - ALPHA)^任务数
    task_poll_time_ewma = weighted_alpha * mean_poll_duration + (1 - weighted_alpha) * 原值
    ```

#### **其他方法**
- **`submit()`**：将统计结果提交到 `WorkerMetrics`。
- **`about_to_park()` 和 `unparked()`**：跟踪工作线程的休眠/唤醒状态。
- **`incr_steal_count()` 等**：统计任务窃取、溢出等事件，用于性能分析。

---

## **在项目中的作用**
该文件是 Tokio 多线程调度器的核心统计模块，通过实时收集任务执行时间、轮询次数等指标，动态调整调度策略（如全局队列检查频率），以优化线程间任务分配和运行时性能。其统计结果同时可用于外部监控，帮助用户诊断运行时行为。
