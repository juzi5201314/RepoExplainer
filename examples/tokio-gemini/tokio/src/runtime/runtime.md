这个文件定义了 Tokio 运行时（`Runtime`）的核心结构和功能。Tokio 运行时是一个提供 I/O 驱动程序、任务调度器、计时器和阻塞池的组件，用于运行异步任务。

**主要组件：**

*   **`Runtime` 结构体：** 这是 Tokio 运行时的核心。它包含以下关键组件：
    *   `scheduler`：任务调度器，可以是单线程或多线程。
    *   `handle`：运行时句柄，用于与运行时交互，例如生成任务。
    *   `blocking_pool`：阻塞池句柄，用于处理阻塞操作。
*   **`Scheduler` 枚举：** 定义了两种类型的任务调度器：
    *   `CurrentThread`：单线程调度器，所有任务都在当前线程上执行。
    *   `MultiThread`：多线程调度器，任务分布在多个线程上执行。
    *   `MultiThreadAlt`：多线程调度器，（如果启用了 `tokio_unstable` 特性）。
*   **`RuntimeFlavor` 枚举：** 表示运行时的类型，包括 `CurrentThread` 和 `MultiThread`。
*   **`Handle` 结构体：** 运行时句柄，用于与运行时交互，例如生成任务。
*   **`EnterGuard` 结构体：** 用于进入运行时上下文，确保在运行时内部执行操作。
*   **`BlockingPool` 结构体：** 用于处理阻塞操作的线程池。

**关键功能：**

*   **`new()`：** 创建一个新的运行时实例，使用默认配置（多线程调度器）。
*   **`handle()`：** 获取运行时的句柄，用于生成任务。
*   **`spawn()`：** 在运行时上生成一个异步任务（`Future`）。
*   **`spawn_blocking()`：** 在阻塞池中生成一个阻塞操作。
*   **`block_on()`：** 在当前线程上运行一个 `Future` 直到完成。这是运行时的入口点。
*   **`enter()`：** 进入运行时上下文，允许在运行时内部执行操作，例如使用 `tokio::spawn`。
*   **`shutdown_timeout()`：** 关闭运行时，等待指定时间，让所有生成的任务停止。
*   **`shutdown_background()`：** 在后台关闭运行时，不等待任务完成。
*   **`metrics()`：** 获取运行时性能指标。

**与项目的关系：**

这个文件定义了 Tokio 异步运行时，是 Tokio 框架的核心组件。它提供了运行异步任务、处理 I/O 操作、管理线程池等功能。其他 Tokio 组件，例如 `tokio::spawn` 和 `tokio::time`，都依赖于 `Runtime`。
