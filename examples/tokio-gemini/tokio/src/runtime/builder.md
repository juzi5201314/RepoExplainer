这个文件定义了 `Builder` 结构体，用于构建 Tokio 运行时，并提供了一系列配置选项。

**主要组成部分：**

*   **`Builder` 结构体：**
    *   `kind`:  运行时类型，可以是单线程 (`CurrentThread`) 或多线程 (`MultiThread`，`MultiThreadAlt`)。
    *   `enable_io`, `enable_time`:  分别控制是否启用 I/O 和时间驱动。
    *   `start_paused`:  控制时钟是否暂停。
    *   `worker_threads`:  多线程运行时的工作线程数量。
    *   `max_blocking_threads`:  阻塞操作（如 `spawn_blocking`）的最大线程数。
    *   `thread_name`, `thread_stack_size`:  线程名称和栈大小。
    *   `after_start`, `before_stop`, `before_park`, `after_unpark`:  线程启动/停止/空闲/恢复时的回调函数。
    *   `before_spawn`, `before_poll`, `after_poll`, `after_termination`:  任务创建/轮询/终止时的回调函数（`tokio_unstable` 特性）。
    *   `keep_alive`:  阻塞线程的保活时间。
    *   `global_queue_interval`:  从全局队列获取任务的间隔。
    *   `event_interval`:  轮询外部事件的间隔。
    *   `local_queue_capacity`:  本地任务队列容量。
    *   `disable_lifo_slot`:  禁用 LIFO 槽（`tokio_unstable` 特性）。
    *   `seed_generator`:  随机数生成器种子。
    *   `metrics_poll_count_histogram_enable`, `metrics_poll_count_histogram`:  任务轮询时间直方图的配置（`tokio_unstable` 特性）。
    *   `unhandled_panic`:  未处理 panic 的行为（`tokio_unstable` 特性）。
*   **`Kind` 枚举：**  定义了运行时类型。
*   **`ThreadNameFn` 类型别名：**  用于线程名称生成函数。
*   **`cfg_unstable!` 宏块：**  包含 `UnhandledPanic` 枚举，定义了未处理 panic 时的行为。
*   **`Builder` 的方法：**
    *   `new_current_thread()`: 创建单线程运行时构建器。
    *   `new_multi_thread()`: 创建多线程运行时构建器。
    *   `new_multi_thread_alt()`: 创建备选的多线程运行时构建器（`tokio_unstable` 特性）。
    *   `new()`:  创建具有默认配置的构建器。
    *   `enable_all()`:  启用所有驱动。
    *   `worker_threads()`, `max_blocking_threads()`, `thread_name()`, `thread_name_fn()`, `thread_stack_size()`:  设置各种配置选项。
    *   `on_thread_start()`, `on_thread_stop()`, `on_thread_park()`, `on_thread_unpark()`, `on_task_spawn()`, `on_before_task_poll()`, `on_after_task_poll()`, `on_task_terminate()`:  设置回调函数。
    *   `build()`:  构建运行时。
    *   `build_local()`:  构建本地运行时（`tokio_unstable` 特性）。
    *   `thread_keep_alive()`, `global_queue_interval()`, `event_interval()`, `unhandled_panic()`, `disable_lifo_slot()`, `rng_seed()`:  设置各种配置选项。
    *   `enable_metrics_poll_time_histogram()`, `metrics_poll_count_histogram_scale()`, `metrics_poll_time_histogram_configuration()`, `metrics_poll_count_histogram_resolution()`, `metrics_poll_count_histogram_buckets()`:  配置任务轮询时间直方图（`tokio_unstable` 特性）。
    *   `local_queue_capacity()`:  设置本地队列容量（`loom` 特性）。
    *   `build_current_thread_runtime()`, `build_current_thread_local_runtime()`, `build_current_thread_runtime_components()`:  构建单线程运行时。
    *   `metrics_poll_count_histogram_builder()`:  构建任务轮询时间直方图构建器。
    *   `enable_io()`, `max_io_events_per_tick()`:  启用 I/O 驱动并配置最大事件数。
    *   `enable_time()`:  启用时间驱动。
    *   `start_paused()`:  控制时钟是否暂停。
    *   `build_threaded_runtime()`, `build_alt_threaded_runtime()`:  构建多线程运行时。
*   **`fmt::Debug` 的实现：**  为 `Builder` 结构体提供了调试输出。

**功能：**

该文件提供了构建 Tokio 运行时的灵活方式。通过 `Builder`，可以自定义运行时的工作线程数量、I/O 和时间驱动、线程名称、回调函数等。`build()` 方法根据配置创建并返回一个 `Runtime` 实例，该实例可用于执行异步任务。

**与其他文件的关系：**

*   依赖于 `crate::runtime::handle::Handle`，`crate::runtime::{blocking, driver, Callback, HistogramBuilder, Runtime, TaskCallback}` 等模块，用于创建运行时组件。
*   `Runtime` 实例由 `Builder` 构建，是 Tokio 异步程序的核心。
*   `Handle` 结构体用于与运行时交互，例如提交任务。
*   `BlockingPool` 用于处理阻塞操作。
*   `driver` 模块提供 I/O 和时间驱动。
*   `scheduler` 模块负责任务调度。
