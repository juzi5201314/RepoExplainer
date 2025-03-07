这个文件定义了 `LocalRuntime` 结构体，它是 Tokio 运行时的一个变体，专门用于在单个线程上运行任务，并且支持 `spawn_local` 函数，该函数允许在没有 `LocalSet` 的情况下生成非 `Send + Sync` 的任务。

**关键组件：**

*   **`LocalRuntime` 结构体：**
    *   `scheduler`:  一个 `LocalRuntimeScheduler` 枚举，目前仅支持 `CurrentThread` 变体，用于调度任务。
    *   `handle`:  `Handle` 结构体，提供对运行时的访问，包括用于生成任务的 `spawn` 方法。
    *   `blocking_pool`:  `BlockingPool` 结构体，用于管理阻塞操作的线程池。
    *   `_phantom`:  一个 `PhantomData` 标记，用于确保 `LocalRuntime` 不是 `Send` 和 `Sync` 的。
*   **`LocalRuntimeScheduler` 枚举：**
    *   `CurrentThread`:  一个变体，表示所有任务都在当前线程上执行。
*   **`from_parts` 函数：**  用于从给定的组件（调度器、句柄和阻塞池）创建 `LocalRuntime` 实例。
*   **`new` 函数：**  创建一个具有默认配置的 `LocalRuntime` 实例。
*   **`handle` 函数：**  返回一个 `Handle` 实例，用于生成任务。
*   **`spawn_local` 函数：**  在运行时上生成一个任务，即使该任务不是线程安全的。
*   **`spawn_blocking` 函数：**  在阻塞线程池中运行一个函数。
*   **`block_on` 函数：**  在运行时上运行一个 Future 到完成。
*   **`block_on_inner` 函数：**  `block_on` 的内部实现，处理任务的执行和追踪。
*   **`enter` 函数：**  进入运行时上下文，允许创建依赖于运行时的类型（如 `Sleep`）和调用 `tokio::spawn`。
*   **`shutdown_timeout` 函数：**  关闭运行时，等待指定的时间，以便所有生成的任务停止。
*   **`shutdown_background` 函数：**  关闭运行时，不等待任何生成的任务停止。
*   **`metrics` 函数：**  返回一个 `RuntimeMetrics` 结构体，提供关于运行时性能的信息。
*   **`Drop` 实现：**  在 `LocalRuntime` 实例被丢弃时，确保在运行时上下文中丢弃在当前线程上生成的任务。

**与其他组件的交互：**

*   `LocalRuntime` 使用 `Handle` 来生成任务，并与 `BlockingPool` 交互以运行阻塞操作。
*   `LocalRuntime` 内部使用 `CurrentThread` 调度器来执行任务。
*   `LocalRuntime` 与 `Builder` 交互以创建具有自定义配置的运行时。

**总结：**
