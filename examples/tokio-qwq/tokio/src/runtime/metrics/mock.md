# 文件说明：`tokio/src/runtime/metrics/mock.rs`

## **目的**  
此文件为 Tokio 运行时的指标（metrics）类型提供模拟实现（mock）。在不需要实际指标收集的场景下（例如性能敏感或非调试环境），这些模拟结构体可以替代真实的指标实现，避免因指标功能引入的额外开销。

---

## **关键组件**

### **1. `SchedulerMetrics`**
- **作用**：模拟调度器（scheduler）的指标收集功能。
- **方法**：
  - `new()`：创建空实例。
  - `inc_remote_schedule_count()`：模拟增加外部调度任务计数（实际为空操作）。
- **实现**：所有方法为空，仅保留接口结构。

### **2. `WorkerMetrics`**
- **作用**：模拟工作者线程（worker thread）的指标收集功能。
- **方法**：
  - `new()`：创建空实例。
  - `from_config(config: &Config)`：通过配置创建实例（忽略配置参数以避免编译警告）。
  - `set_queue_depth()`、`set_thread_id()`：模拟设置队列深度和线程 ID（实际为空操作）。
- **实现**：所有方法为空，仅保留接口结构。

### **3. `MetricsBatch`**
- **作用**：模拟批量指标收集操作，用于记录线程的运行状态和任务处理事件。
- **方法**：
  - `new()`：通过 `WorkerMetrics` 创建实例。
  - `submit()`、`about_to_park()`、`unparked()` 等：模拟提交指标、线程休眠/唤醒事件（实际为空操作）。
  - 多线程环境下的额外方法（如 `incr_steal_count`）：通过 `cfg_rt_multi_thread!` 宏条件编译添加，但同样为空操作。
- **实现**：所有方法为空，仅保留接口结构。

### **4. `HistogramBuilder`**
- **作用**：模拟直方图（histogram）构建器，用于统计任务执行时间等分布数据。
- **特性**：实现 `Default` 和 `Clone`，但所有操作为空。

---

## **实现细节**
- **模拟逻辑**：所有方法均为空实现（`{}`），仅保留接口签名，确保代码兼容性。
- **条件编译**：通过 `cfg_rt_multi_thread!` 宏为多线程场景添加额外方法，但内容仍为空。
- **配置兼容性**：`WorkerMetrics::from_config` 中通过引用 `config.metrics_poll_count_histogram` 避免编译器因未使用配置项而报错。

---

## **项目中的角色**
此文件为 Tokio 运行时提供无功能的指标模拟实现，允许在不启用指标收集功能时减少运行时的内存和性能开销，是 Tokio 模块化设计和按需编译优化的关键组成部分。
