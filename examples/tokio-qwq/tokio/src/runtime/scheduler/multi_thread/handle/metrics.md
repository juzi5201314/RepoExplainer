# 文件说明：`metrics.rs`

## 功能概述  
该文件为 Tokio 多线程调度器的 `Handle` 结构体提供与运行时指标相关的功能实现。通过暴露一系列方法，允许用户查询调度器的内部状态，包括线程数量、任务队列深度、阻塞线程统计等，主要用于监控和调试 Tokio 运行时的性能。

---

## 核心组件与方法  

### 基础指标方法  
1. **`num_workers()`**  
   返回调度器中活跃的工作者线程数量，通过 `shared.worker_metrics` 的长度计算得出。

2. **`num_alive_tasks()`**  
   获取当前运行时中存活的任务数量，通过 `shared.owned` 字段调用内部方法实现。

3. **`injection_queue_depth()`**  
   返回注入队列（用于跨线程任务调度）的当前深度，反映任务分配的负载情况。

---

### 高级指标（受 `cfg_unstable_metrics` 宏控制）  
当启用实验性指标功能时，提供以下扩展方法：  

#### 线程与任务统计  
- **`num_blocking_threads()`**  
  计算阻塞线程池中活跃线程的数量（排除工作者线程），通过 `blocking_spawner` 的线程计数减去工作者线程数得出。

- **`num_idle_blocking_threads()`**  
  获取阻塞线程池中空闲线程的数量，直接调用 `blocking_spawner` 的内部方法。

- **`spawned_tasks_count()`**  
  返回自运行时启动以来创建的总任务数（64位系统下支持大数值统计）。

#### 调度器与工作者指标  
- **`scheduler_metrics()`**  
  返回调度器级的全局指标（如任务分配次数、负载均衡统计），通过 `shared.scheduler_metrics` 提供。

- **`worker_metrics(worker: usize)`**  
  获取指定工作者线程的详细指标（如任务执行时间、队列操作次数）。

- **`worker_local_queue_depth(worker: usize)`**  
  返回指定工作者线程本地队列的当前深度，反映任务处理的局部负载。

- **`blocking_queue_depth()`**  
  获取阻塞任务队列的当前深度，用于监控阻塞操作的堆积情况。

---

## 实现细节  
- **配置宏 `cfg_unstable_metrics`**  
  通过条件编译控制指标功能的启用，确保实验性功能不会影响核心代码的稳定性。  
- **依赖结构**  
  依赖 `Handle` 的 `shared` 字段（包含运行时共享状态）和 `blocking_spawner`（阻塞线程池管理器）来获取底层数据。

---

## 项目中的角色  
该文件是 Tokio 多线程调度器监控系统的核心组件，通过暴露运行时内部指标，为性能分析、负载均衡优化和故障排查提供数据支持，是运行时可观察性（Observability）的重要实现部分。
