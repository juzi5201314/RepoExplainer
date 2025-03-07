### 代码文件解释

#### **文件目的**
该文件是 Tokio 运行时多线程调度器的统计模块，负责收集和维护工作线程的运行时统计信息，用于动态调整调度策略和提供运行时指标。通过跟踪任务处理时间、负载均衡等关键指标，优化多线程任务调度的性能。

---

#### **关键组件**

1. **`Stats` 结构体**
   - **功能**：存储统计信息和动态调整参数。
   - **核心字段**：
     - `batch`: 用于聚合和上报运行时指标的批处理对象。
     - `task_poll_time_ewma`: 任务处理时间的指数加权移动平均值（EWMA），用于动态调整调度间隔。
   - **方法**：
     - `new()`: 初始化统计对象，使用预设目标值初始化 EWMA。
     - `tuned_global_queue_interval()`: 根据当前 EWMA 计算任务处理间隔，动态调整全局队列检查频率。
     - `submit()`: 将统计结果提交到工作线程的指标对象。
     - `start/end_processing_scheduled_tasks()`: 跟踪批量任务处理的开始和结束时间，更新 EWMA。

2. **`Ephemeral` 结构体**
   - **功能**：维护临时状态，用于单次任务处理批次的统计。
   - **核心字段**：
     - `processing_scheduled_tasks_started_at`: 批量任务处理的开始时间。
     - `tasks_polled_in_batch`: 当前批次处理的任务数量。
   - **方法**：
     - `new()`: 初始化临时状态对象。

3. **常量与配置**
   - `TASK_POLL_TIME_EWMA_ALPHA`: EWMA 的衰减系数（0.1），控制历史数据与新数据的权重。
   - `TARGET_GLOBAL_QUEUE_INTERVAL`: 目标全局队列检查间隔（200 微秒）。
   - `MAX_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`: 单次检查间隔内处理任务的最大数量（127）。

---

#### **工作流程**
1. **初始化**：
   - `Stats::new()` 初始化时，使用目标值预设 `task_poll_time_ewma`，确保初始值合理。

2. **任务处理统计**：
   - 调用 `start_processing_scheduled_tasks()` 记录批次开始时间。
   - 每次任务处理时调用 `start_poll()` 和 `end_poll()`，累加任务计数。
   - 批次结束后，通过 `end_processing_scheduled_tasks()` 计算当前批次的平均任务处理时间，并更新 EWMA。

3. **动态调整**：
   - `tuned_global_queue_interval()` 根据当前 EWMA 计算任务处理间隔，确保在合理范围内（如不超过 `MAX_TASKS_POLLED_PER_GLOBAL_QUEUE_INTERVAL`）。

4. **指标上报**：
   - `submit()` 将统计结果提交到 `WorkerMetrics`，供运行时全局汇总和监控。

---

#### **在项目中的角色**
该文件是 Tokio 多线程调度器的核心统计模块，通过实时跟踪任务处理时间和负载情况，动态调整调度策略（如全局队列检查频率），优化多线程任务分配的效率，确保运行时资源的高效利用。
