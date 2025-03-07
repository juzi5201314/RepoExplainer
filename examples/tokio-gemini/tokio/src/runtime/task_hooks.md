这个文件定义了 Tokio 运行时中用于任务钩子的结构和相关功能。它的主要目的是允许用户在任务的生命周期中注册回调函数，以便在任务创建、轮询开始、轮询结束和终止时执行自定义逻辑。

**关键组件：**

*   **`TaskHooks` 结构体:**
    *   这是一个结构体，用于存储各种任务相关的回调函数。
    *   `task_spawn_callback`:  一个可选的回调函数，在任务被创建时调用。
    *   `task_terminate_callback`: 一个可选的回调函数，在任务终止时调用。
    *   `before_poll_callback` 和 `after_poll_callback`:  这两个回调函数仅在 `tokio_unstable` 特性启用时可用。它们分别在任务轮询开始和结束时调用。
    *   `from_config` 方法：根据配置创建 `TaskHooks` 实例，从 `Config` 中获取回调函数。
    *   `spawn` 方法：在任务创建时调用 `task_spawn_callback`。
    *   `poll_start_callback` 和 `poll_stop_callback` 方法：分别在任务轮询开始和结束时调用相应的回调函数（如果已设置）。

*   **`TaskMeta` 结构体:**
    *   这个结构体用于向回调函数提供任务的元数据。
    *   `id`:  任务的唯一 ID。
    *   `_phantom`:  一个 `PhantomData` 字段，用于确保 `TaskMeta` 结构体是 `Send` 和 `Sync` 的。

*   **`TaskCallback` 类型别名:**
    *   定义了一个类型别名，表示任务回调函数的类型。它是一个 `Arc` 包装的闭包，接受一个 `TaskMeta` 引用作为参数，并且是 `Send` 和 `Sync` 的。

**功能和作用：**

*   **任务生命周期钩子:**  `TaskHooks` 允许用户在任务的生命周期中的关键点（创建、轮询、终止）插入自定义逻辑。
*   **配置灵活性:**  `TaskHooks` 的配置来自 `Config` 结构体，这使得用户可以通过配置来启用或禁用特定的钩子，并提供自定义的回调函数。
*   **`tokio_unstable` 特性:**  `before_poll_callback` 和 `after_poll_callback` 仅在启用 `tokio_unstable` 特性时可用，这表明它们是实验性的，可能会在未来的 Tokio 版本中发生变化。
*   **元数据传递:**  `TaskMeta` 结构体向回调函数提供了任务的 ID，这使得回调函数可以识别和操作特定的任务。

**与项目的整体关系：**

这个文件是 Tokio 运行时的一部分，它提供了任务钩子机制，允许用户在任务的生命周期中添加自定义行为。它通过 `Config` 结构体与运行时配置集成，并使用 `TaskMeta` 结构体传递任务元数据给回调函数。这个文件增强了 Tokio 的可扩展性和灵活性，允许用户监控、调试和定制任务的行为。
