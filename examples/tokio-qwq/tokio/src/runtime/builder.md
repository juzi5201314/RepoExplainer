# Tokio 运行时构建器 (Builder) 模块详解

## **文件作用**
此文件定义了 Tokio 运行时的构建器 (`Builder`)，用于配置和创建 Tokio 异步运行时。通过链式调用配置方法，开发者可以灵活定制运行时的行为，包括线程池大小、调度策略、资源限制等核心参数。

---

## **核心组件**

### **1. `Builder` 结构体**
- **配置参数**：
  - **运行时类型 (`kind`)**：支持单线程 (`CurrentThread`) 和多线程 (`MultiThread`) 模式。
  - **I/O 和时钟驱动 (`enable_io`, `enable_time`)**：控制是否启用 I/O 操作和定时器功能。
  - **线程池参数**：
    - `worker_threads`：工作线程数量（默认为 CPU 核心数）。
    - `max_blocking_threads`：阻塞线程池的最大容量（默认 512）。
  - **线程配置**：
    - `thread_name`：线程名称生成函数。
    - `thread_stack_size`：线程栈大小（默认 2MB）。
  - **回调函数**：在线程生命周期（启动/停止）、任务调度（前/后）等阶段执行自定义逻辑。

- **关键方法**：
  - **初始化方法**：
    - `new_current_thread()`：创建单线程运行时构建器。
    - `new_multi_thread()`：创建多线程运行时构建器。
  - **配置方法**：
    - `worker_threads()`：设置工作线程数量。
    - `enable_all()`：同时启用 I/O 和时钟驱动。
    - `on_thread_start()`/`on_thread_stop()`：注册线程生命周期回调。
    - `thread_keep_alive()`：设置阻塞线程空闲超时时间。
  - **构建方法**：
    - `build()`：根据配置生成运行时实例。

### **2. 调度器配置**
- **单线程调度器 (`CurrentThread`)**：
  - 适用于需要直接驱动的场景（如 `block_on`）。
  - 内部使用 `driver` 处理 I/O 和定时器事件。
- **多线程调度器 (`MultiThread`)**：
  - 支持工作窃取（Work-Stealing）算法。
  - 可配置 `global_queue_interval` 控制全局队列轮询间隔。
  - 通过 `disable_lifo_slot` 禁用 LIFO 优化（实验性功能）。

### **3. 不稳定特性**
- **未处理 panic 处理 (`unhandled_panic`)**：
  - 支持 `Ignore`（默认）或 `ShutdownRuntime` 策略。
- **任务指标 (`metrics_poll_time_histogram`)**：
  - 统计任务调度时间分布，支持线性或对数分桶配置。

---

## **关键流程**
1. **构建器初始化**：
   - 调用 `new_current_thread()` 或 `new_multi_thread()` 获取初始配置。
2. **配置链式调用**：
   - 例如：`.worker_threads(4).enable_all().thread_name("my-pool")`。
3. **运行时创建**：
   - `build()` 方法根据配置生成 `Runtime` 或 `LocalRuntime` 实例。
   - 内部初始化驱动（`Driver`）、线程池和调度器。

---

## **与其他模块的交互**
- **驱动模块 (`driver`)**：管理 I/O 和定时器事件循环。
- **阻塞池 (`blocking::BlockingPool`)**：处理阻塞任务（如文件 I/O）。
- **调度器 (`scheduler`)**：实现任务分发和线程管理逻辑。
- **回调 (`Callback`/`TaskCallback`)**：允许用户插入自定义监控或日志逻辑。

---

## **文件在项目中的角色**