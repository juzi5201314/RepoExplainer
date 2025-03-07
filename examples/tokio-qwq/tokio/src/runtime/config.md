# 配置文件 `config.rs` 详解

## 功能概述  
该文件定义了 Tokio 运行时的核心配置参数 `Config`，用于控制多线程调度器的行为、任务调度策略、事件轮询间隔以及运行时的监控指标等。这些配置选项允许开发者根据具体需求调整运行时的性能和行为。

---

## 核心组件与字段说明

### 1. **任务调度相关配置**
- **`global_queue_interval`**  
  类型：`Option<u32>`  
  作用：设置工作者线程从全局队列拉取任务的间隔（以 tick 为单位）。`None` 表示禁用全局队列拉取。

- **`event_interval`**  
  类型：`u32`  
  作用：控制工作者线程检查 I/O 或定时器事件的频率。值越小，事件响应越及时，但可能增加 CPU 使用率。

- **`local_queue_capacity`**  
  类型：`usize`  
  作用：指定每个工作者线程本地任务队列的容量。较大的值可减少线程间竞争，但会增加内存占用。

- **`disable_lifo_slot`**  
  类型：`bool`  
  作用：是否禁用多线程调度器的 LIFO（后进先出）槽。LIFO 槽用于优化任务传递场景，但当前不可被其他线程窃取（未来可能支持）。

---

### 2. **回调钩子（Callbacks）**
提供在特定事件发生时执行自定义逻辑的能力：
- **任务生命周期钩子**  
  - `before_spawn`: 任务创建前触发。
  - `after_termination`: 任务终止后触发。
- **线程状态钩子**  
  - `before_park`: 线程进入休眠前触发。
  - `after_unpark`: 线程被唤醒后触发。
- **不稳定特性钩子（需 `tokio_unstable`）**  
  - `before_poll`/`after_poll`: 在任务 `poll` 方法执行前后触发。

---

### 3. **调试与监控配置**
- **`seed_generator`**  
  类型：`RngSeedGenerator`  
  作用：通过设置随机数种子使运行时行为可复现，适用于测试场景。

- **`metrics_poll_count_histogram`**  
  类型：`Option<crate::runtime::HistogramBuilder>`  
  作用：配置轮询时间直方图，用于统计任务 `poll` 的耗时分布。

- **`unhandled_panic`**  
  类型：`crate::runtime::UnhandledPanic`（需 `tokio_unstable`）  
  作用：定义未处理任务 panic 的处理策略（如终止运行时或仅记录日志）。

---

### 4. **条件编译与稳定性**
- 使用 `cfg_attr` 和 `cfg` 宏控制代码的编译条件：
  - 对于非全功能模式或 WebAssembly 目标，允许未使用的代码片段。
  - 不稳定特性（如 `before_poll`）仅在启用 `tokio_unstable` 时生效。

---

## 在项目中的角色  
该文件是 Tokio 运行时配置的核心，通过 `Config` 结构体集中管理多线程调度器的调度策略、任务行为、监控指标及调试选项。它为运行时的初始化提供了灵活的参数控制，确保开发者能够根据具体场景（如性能优化、测试或调试）调整运行时行为，是 Tokio 内部调度和资源管理的基础配置模块。
