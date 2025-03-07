这个文件定义了 `yield_now` 函数，该函数允许 Tokio 运行时中的任务主动让出执行权，以便其他任务能够获得 CPU 时间。

**主要组成部分：**

1.  **`yield_now()` 函数:**
    *   这是一个 `async` 函数，意味着它可以在 Tokio 运行时中被 `await`。
    *   它的作用是让当前任务暂停执行，并将控制权交还给 Tokio 运行时。
    *   当任务 `await` `yield_now()` 时，它会被重新添加到待处理任务队列的末尾。
    *   运行时可以选择在稍后某个时间点重新调度该任务。

2.  **`YieldNow` 结构体:**
    *   这是一个内部结构体，实现了 `Future` trait。
    *   `yield_now()` 函数内部使用 `YieldNow` 结构体来实现让出执行权的功能。
    *   `yielded: bool` 字段用于跟踪任务是否已经让出过执行权。

3.  **`Future` trait 的实现 (针对 `YieldNow`):**
    *   `poll()` 方法是 `Future` trait 的核心。
    *   首先，调用 `crate::trace::trace_leaf(cx)` (如果启用了跟踪功能)。
    *   如果 `yielded` 标志为 `true`，则任务已经让出过执行权，`poll()` 方法返回 `Poll::Ready(())`，表示 future 完成。
    *   如果 `yielded` 标志为 `false`，则将 `yielded` 设置为 `true`。
    *   调用 `context::defer(cx.waker())`，将当前任务的 `waker` 延迟到稍后执行。这使得 Tokio 运行时能够重新调度该任务。
    *   返回 `Poll::Pending`，表示 future 尚未完成，需要稍后再次 `poll`。

**如何融入项目：**

*   `yield_now()` 函数是 Tokio 运行时的一个关键组成部分，用于实现任务间的协作和公平调度。
*   它允许长时间运行的任务定期让出执行权，避免独占 CPU 资源，从而提高整个应用程序的响应性和吞吐量。
*   开发人员可以在需要时使用 `yield_now().await` 来手动控制任务的执行流程，例如，在循环中定期让出执行权，或者在等待某些条件时让出执行权。
