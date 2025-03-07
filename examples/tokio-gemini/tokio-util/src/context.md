这个文件定义了 `TokioContext` 结构体和 `RuntimeExt` trait，它们的主要目的是允许在非 Tokio 运行时中运行需要 Tokio 上下文的 future。这在需要在不支持 Tokio 上下文的执行器或运行时中使用基于 Tokio 的库时非常有用。

**关键组件：**

*   **`TokioContext<F>` 结构体:**
    *   它是一个包装器，包含一个需要运行的 future (`inner`) 和一个 Tokio 运行时句柄 (`handle`)。
    *   `#[pin]` 属性用于确保 `inner` future 可以被安全地固定。
    *   `handle` 允许在 `poll` 方法中进入 Tokio 运行时上下文。
    *   `new` 方法用于创建 `TokioContext` 实例，接收一个 future 和一个 Tokio 运行时句柄。
    *   `handle` 方法返回对运行时句柄的引用。
    *   `into_inner` 方法用于从 `TokioContext` 中提取原始的 future。
    *   实现了 `Future` trait，在 `poll` 方法中，它首先使用 `handle.enter()` 进入 Tokio 运行时上下文，然后调用内部 future 的 `poll` 方法。

*   **`RuntimeExt` trait:**
    *   这是一个扩展 trait，为 `tokio::runtime::Runtime` 提供了 `wrap` 方法。
    *   `wrap` 方法创建一个 `TokioContext` 实例，将给定的 future 与当前运行时的上下文关联起来。

*   **`impl RuntimeExt for Runtime`:**
    *   为 `tokio::runtime::Runtime` 实现了 `RuntimeExt` trait。
    *   `wrap` 方法的具体实现，用于创建 `TokioContext` 实例。

**工作原理：**

1.  创建一个 Tokio 运行时。
2.  使用 `Runtime::handle()` 获取运行时的句柄。
3.  创建一个需要 Tokio 上下文的 future。
4.  使用 `RuntimeExt::wrap` 方法（或 `TokioContext::new`）将 future 和运行时句柄包装在 `TokioContext` 中。
5.  在另一个运行时（可能不支持 Tokio 上下文）中运行 `TokioContext` 实例。
6.  当 `TokioContext` 的 `poll` 方法被调用时，它会使用 `handle.enter()` 进入 Tokio 运行时上下文，然后调用内部 future 的 `poll` 方法。

**与项目的关系：**

这个文件提供了一个工具，用于在 Tokio 之外的运行时中执行依赖于 Tokio 上下文的 future。它增强了 `tokio-util` crate 的灵活性，允许在更广泛的环境中使用 Tokio 库。
