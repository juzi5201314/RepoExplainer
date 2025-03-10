这个文件定义了 Tokio 运行时中使用的几个错误字符串常量。

*   `CONTEXT_MISSING_ERROR`:  这个常量表示当代码尝试在没有 Tokio 运行时上下文的情况下运行时发生的错误。这意味着代码试图在没有 Tokio 运行时实例的情况下执行 Tokio 相关的操作，例如启动一个任务或使用 Tokio 的异步功能。
*   `RUNTIME_SHUTTING_DOWN_ERROR`:  这个常量表示当 Tokio 运行时正在关闭时发生的错误。当运行时正在关闭时，它可能无法驱动定时器或其他依赖于运行时的操作。
*   `THREAD_LOCAL_DESTROYED_ERROR`:  这个常量表示当 Tokio 运行时的线程局部变量已被销毁时发生的错误。这通常发生在其他线程局部变量的析构函数中，并且 Tokio 运行时的上下文不再可用。

这些常量用于在 Tokio 库中生成清晰的错误消息，帮助开发者理解和调试与 Tokio 运行时相关的错误。它们被用于在运行时出现特定情况时，提供有意义的错误信息，例如当没有运行时上下文可用时，或者当运行时正在关闭时。
