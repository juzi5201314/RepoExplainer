这个文件定义了 Tokio 运行时（runtime）的调度器（scheduler）模块，负责管理任务的执行。它根据不同的配置选项（features）提供了不同的调度器实现，包括单线程和多线程调度器。

**主要组成部分：**

1.  **模块声明和引入：**
    *   `cfg_rt!` 和 `cfg_rt_multi_thread!` 宏用于根据是否启用 `rt` 和 `rt-multi-thread` 特性来条件编译代码。
    *   引入了 `current_thread`, `multi_thread`, `multi_thread_alt`, `block_in_place` 等模块，这些模块分别实现了不同的调度器。
    *   `use` 语句引入了这些模块中的关键类型和函数，例如 `CurrentThread`, `MultiThread`, `block_in_place`。
    *   引入了 `driver` 模块，用于驱动运行时。
    *   引入了 `TaskHooks`，用于任务钩子。

2.  **`Handle` 枚举：**
    *   `Handle` 枚举是调度器的句柄，用于访问和控制运行时。
    *   它根据不同的特性，包含不同的变体：
        *   `CurrentThread`: 单线程运行时句柄。
        *   `MultiThread`: 多线程运行时句柄。
        *   `MultiThreadAlt`:  多线程运行时句柄（如果启用了 `tokio_unstable` 特性）。
        *   `Disabled`:  如果未启用 `rt` 特性，则使用此变体。
    *   `Handle` 实现了 `Clone` 和 `Debug` trait。

3.  **`Context` 枚举：**
    *   `Context` 枚举表示运行时的上下文。
    *   它与 `Handle` 类似，根据不同的特性，包含不同的变体：
        *   `CurrentThread`: 单线程运行时上下文。
        *   `MultiThread`: 多线程运行时上下文。
        *   `MultiThreadAlt`: 多线程运行时上下文（如果启用了 `tokio_unstable` 特性）。

4.  **`Handle` 的方法实现：**
    *   `driver()`:  获取运行时驱动程序的句柄。
    *   `current()`:  获取当前线程的 `Handle`。
    *   `blocking_spawner()`:  获取阻塞任务的生成器。
    *   `is_local()`:  判断是否是本地运行时。
    *   `can_spawn_local_on_local_runtime()`:  判断是否可以在本地运行时上生成本地任务。
    *   `spawn()`:  生成一个任务。
    *   `spawn_local()`:  生成一个本地任务（仅限 `CurrentThread`）。
    *   `shutdown()`:  关闭运行时。
    *   `seed_generator()`:  获取随机数种子生成器。
    *   `as_current_thread()`:  将 `Handle` 转换为 `CurrentThread` 的句柄。
    *   `hooks()`:  获取任务钩子。
    *   `expect_multi_thread_alt()`:  获取 `MultiThreadAlt` 句柄（仅限 `rt-multi-thread` 和 `tokio_unstable`）。
    *   `num_workers()`:  获取工作线程的数量。
    *   `num_alive_tasks()`: 获取存活任务的数量。
    *   `injection_queue_depth()`: 获取注入队列的深度。
    *   `spawned_tasks_count()`: 获取已生成任务的数量（如果启用了 `cfg_64bit_metrics`）。
    *   `num_blocking_threads()`: 获取阻塞线程的数量。
    *   `num_idle_blocking_threads()`: 获取空闲阻塞线程的数量。
    *   `scheduler_metrics()`: 获取调度器指标。
    *   `worker_metrics()`: 获取工作线程指标。
    *   `worker_local_queue_depth()`: 获取工作线程本地队列深度。
    *   `blocking_queue_depth()`: 获取阻塞队列深度。

5.  **`Context` 的方法实现：**
    *   `expect_current_thread()`:  获取 `CurrentThread` 的上下文。
    *   `defer()`:  延迟执行一个任务。
    *   `expect_multi_thread()`:  获取 `MultiThread` 的上下文。
    *   `expect_multi_thread_alt()`:  获取 `MultiThreadAlt` 的上下文。

6.  **条件编译：**
    *   使用 `cfg_rt!` 和 `cfg_rt_multi_thread!` 宏，根据特性启用或禁用代码块。
    *   使用 `cfg_unstable!` 宏，启用不稳定特性相关的代码。
    *   使用 `cfg_64bit_metrics!` 宏，启用 64 位指标相关的代码。
    *   使用 `cfg_not_rt!` 宏，在未启用 `rt` 特性时，提供 `Handle::current()` 的实现。

**与其他文件的关系：**

*   `current_thread`, `multi_thread`, `multi_thread_alt` 模块：这些模块实现了具体的调度器逻辑，`mod.rs` 负责将它们组合起来，并提供统一的接口。
*   `driver` 模块：`mod.rs` 使用 `driver` 模块来驱动运行时。
*   `crate::runtime` 模块：`mod.rs` 属于 `crate::runtime` 模块的一部分，是运行时核心组件之一。
*   `crate::task` 模块：`mod.rs` 使用 `JoinHandle` 来管理任务。
*   `crate::future` 模块：`mod.rs` 使用 `Future` trait 来表示异步任务。
*   `crate::loom::sync` 模块：`mod.rs` 使用 `Arc` 来实现线程安全。
