### 代码文件解释

#### 文件目的
该文件为Tokio运行时的多线程调度器提供指标监控功能，通过`Handle`结构体暴露一系列方法，用于获取运行时的线程、任务和队列状态信息。这些指标帮助开发者监控资源使用情况、优化性能或排查问题。

#### 关键组件
1. **线程相关指标**
   - `num_workers()`: 返回活跃工作线程数量，通过`WorkerMetrics`集合的长度计算。
   - `num_blocking_threads()`: 计算阻塞线程池中非工作线程的线程数，通过`blocking_spawner`的总线程数减去工作线程数。
   - `num_idle_blocking_threads()`: 获取阻塞线程池中空闲线程的数量。

2. **任务相关指标**
   - `num_alive_tasks()`: 返回当前存活的任务数量。
   - `spawned_tasks_count()`: 在64位系统下统计已创建任务的总数（使用`u64`类型）。

3. **队列深度指标**
   - `injection_queue_depth()`: 获取全局注入队列的当前深度。
   - `worker_local_queue_depth(worker)`: 返回指定工作线程本地队列的深度。
   - `blocking_queue_depth()`: 获取阻塞任务队列的深度。

4. **调度器与工作线程指标**
   - `scheduler_metrics()`: 返回调度器级别的综合指标（如任务分配、负载均衡等）。
   - `worker_metrics(worker)`: 提供特定工作线程的详细指标（如任务执行时间、队列状态等）。

#### 实现细节
- **依赖结构**
  - `Handle`：运行时句柄，持有对共享状态（如`shared`和`blocking_spawner`）的引用。
  - `SchedulerMetrics` 和 `WorkerMetrics`：分别存储调度器和工作线程的统计信息。
  - `blocking_spawner`：阻塞线程池的管理器，提供线程和队列状态的查询接口。

- **宏配置**
  - `cfg_64bit_metrics!`：在64位系统下启用大整数计数器（如`spawned_tasks_count`）。
  - `cfg_unstable_metrics!`：可能用于启用实验性指标功能（如`Spawner`的线程计数方法）。

#### 项目中的角色
该文件是Tokio多线程调度器的监控模块核心组件，通过暴露运行时内部状态的指标接口，为性能分析、资源管理和错误诊断提供数据支持，确保运行时高效稳定地处理异步任务和阻塞操作。
``` 
