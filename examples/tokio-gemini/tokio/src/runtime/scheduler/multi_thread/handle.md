这个文件定义了 `Handle` 结构体，它是 Tokio 运行时多线程调度器的句柄。它提供了与调度器交互的接口，例如生成任务和关闭运行时。

**关键组件：**

*   `Handle` 结构体：
    *   `shared`:  `worker::Shared` 类型的字段，用于与工作线程共享数据。
    *   `driver`:  `driver::Handle` 类型的字段，用于驱动程序。
    *   `blocking_spawner`: `blocking::Spawner` 类型的字段，用于生成阻塞任务。
    *   `seed_generator`: `RngSeedGenerator` 类型的字段，用于生成随机数种子。
    *   `task_hooks`: `TaskHooks` 类型的字段，用于用户提供的钩子函数，在任务生命周期的不同阶段调用。
*   `spawn` 方法：将一个 `Future` 生成到线程池中。
*   `shutdown` 方法：关闭运行时。
*   `bind_new_task` 方法：将新的任务绑定到调度器，并返回一个 `JoinHandle`。
*   `cfg_unstable!` 块：包含一个 `owned_id` 方法，该方法仅在启用 `unstable` 特性时可用，用于获取拥有的 ID。
*   `fmt::Debug` 实现：为 `Handle` 结构体提供调试输出。

**功能：**

*   **任务生成：** `spawn` 方法是核心功能，它允许用户将 `Future` 提交给运行时执行。
*   **运行时控制：** `shutdown` 方法允许用户优雅地关闭运行时。
*   **任务绑定：** `bind_new_task` 方法负责将新创建的任务与调度器关联起来，并处理任务的生命周期管理。
*   **配置和扩展：**  `seed_generator` 和 `task_hooks` 字段允许配置运行时行为和扩展功能。

**与其他组件的关联：**

*   与 `worker` 模块交互，用于任务的实际执行。
*   与 `driver` 模块交互，用于驱动程序。
*   与 `blocking` 模块交互，用于处理阻塞任务。
*   与 `task` 模块交互，用于创建和管理任务。
*   与 `RngSeedGenerator` 交互，用于生成随机数。
*   与 `TaskHooks` 交互，用于用户自定义的任务钩子。
