这个文件 `context.rs` 实现了 Tokio 运行时（runtime）的线程局部上下文管理。它的主要目的是在 Tokio 运行时中存储和访问与当前线程相关的各种信息，例如线程 ID、调度器、当前任务 ID、运行时状态、随机数生成器和预算。

**关键组件：**

*   **`Context` 结构体：**
    *   `thread_id`： 存储当前线程的唯一标识符。
    *   `current`： 存储当前运行时句柄，用于生成任务、访问驱动程序等。
    *   `scheduler`： 存储调度器的内部上下文。
    *   `current_task_id`： 存储当前正在执行的任务的 ID。
    *   `runtime`： 跟踪当前线程是否正在驱动运行时。
    *   `rng`： 随机数生成器。
    *   `budget`： 跟踪任务在让步给调度器之前可以执行的“工作”量。
    *   `trace`： (仅在特定配置下) 用于任务转储的上下文。
*   **`CONTEXT` 线程局部静态变量：**
    *   使用 `tokio_thread_local!` 宏定义，确保每个线程都有自己的 `Context` 实例。
    *   初始化 `Context` 结构体，并设置默认值。
*   **各种函数：**
    *   `thread_rng_n(n: u32)`： 获取线程局部的随机数生成器，并生成一个 0 到 n-1 之间的随机数。
    *   `budget<R>(f: impl FnOnce(&Cell<coop::Budget>) -> R)`： 允许访问和修改当前线程的预算。
    *   `thread_id()`： 获取当前线程的 ID。
    *   `set_current_task_id(id: Option<Id>)`： 设置当前任务的 ID。
    *   `current_task_id()`： 获取当前任务的 ID。
    *   `defer(waker: &Waker)`： 将一个 `Waker` 延迟到调度器。
    *   `set_scheduler<R>(v: &scheduler::Context, f: impl FnOnce() -> R)`： 设置调度器的上下文。
    *   `with_scheduler<R>(f: impl FnOnce(Option<&scheduler::Context>) -> R)`： 允许访问调度器的上下文。
    *   `with_trace<R>(f: impl FnOnce(&trace::Context) -> R)`： (仅在特定配置下) 允许访问任务转储上下文。

**与其他组件的交互：**

*   **`crate::loom::thread`：** 用于线程相关的操作，例如获取线程 ID。
*   **`crate::task::coop`：** 用于管理任务的协作预算。
*   **`crate::util::rand`：** 用于随机数生成。
*   **`crate::runtime`：** 与 Tokio 运行时核心组件交互，例如调度器、任务等。
*   **`crate::runtime::scheduler`：** 调度器上下文。
*   **`crate::runtime::task`：** 任务 ID。

**作用：**
