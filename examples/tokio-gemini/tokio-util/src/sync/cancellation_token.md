这个文件定义了一个异步可等待的 `CancellationToken`，它允许向一个或多个任务发出取消请求。

**主要组成部分：**

*   **`CancellationToken` 结构体：**
    *   这是取消令牌的主要结构体。它包含一个 `Arc<tree_node::TreeNode>`，用于管理取消状态和关联的任务。
    *   实现了 `Clone`，`Drop`，`Default` 和 `Debug` trait。
    *   `Clone` 实现允许创建令牌的副本，这些副本共享相同的取消状态。
    *   `Drop` 实现减少内部 `TreeNode` 的引用计数。
    *   `Default` 实现创建一个新的 `CancellationToken`。
    *   `Debug` 实现用于调试输出。
    *   `new()`: 创建一个新的未取消的 `CancellationToken`。
    *   `child_token()`: 创建一个子令牌，当父令牌被取消时，子令牌也会被取消，但取消子令牌不会取消父令牌。
    *   `cancel()`: 取消 `CancellationToken` 及其所有子令牌。
    *   `is_cancelled()`: 检查令牌是否已被取消。
    *   `cancelled()`: 返回一个 `Future`，该 `Future` 在令牌被取消时完成。
    *   `cancelled_owned()`: 返回一个拥有令牌的 `Future`，在令牌被取消时完成。
    *   `drop_guard()`: 创建一个 `DropGuard`，当 `DropGuard` 被丢弃时，会取消令牌。
    *   `run_until_cancelled()`: 运行一个 `Future` 直到令牌被取消或 `Future` 完成。

*   **`WaitForCancellationFuture<'a>` 结构体：**
    *   一个 `Future`，当关联的 `CancellationToken` 被取消时，它会完成。
    *   它持有对 `CancellationToken` 的引用。
    *   `poll()` 方法检查令牌是否被取消，如果已取消，则返回 `Poll::Ready`。否则，它会轮询内部的 `tokio::sync::futures::Notified` future，直到收到通知或令牌被取消。

*   **`WaitForCancellationFutureOwned` 结构体：**
    *   与 `WaitForCancellationFuture` 类似，但它拥有 `CancellationToken`。
    *   使用 `MaybeDangling` 来处理生命周期问题，确保在 `Future` 结束前 `CancellationToken` 仍然有效。
    *   `new()` 方法创建 `WaitForCancellationFutureOwned`。
    *   `new_future()` 方法创建一个 `tokio::sync::futures::Notified<'static>` future，该 future 依赖于 `CancellationToken` 的内部状态。
    *   `poll()` 方法与 `WaitForCancellationFuture` 类似，但它使用拥有的 `CancellationToken`。

*   **`guard` 模块：**
    *   包含 `DropGuard` 结构体，用于在 `DropGuard` 被丢弃时取消令牌。

*   **`tree_node` 模块：**
    *   包含 `TreeNode` 结构体，用于管理取消状态和关联的任务。

**功能和作用：**

*   允许任务注册以响应取消信号。
*   提供了一种安全的方式来取消任务，并确保在取消时释放资源。
*   支持创建子令牌，以便更精细地控制取消范围。
*   提供 `Future`，用于等待取消信号。
*   提供 `DropGuard`，用于在作用域结束时自动取消令牌。

**与其他组件的交互：**

*   `CancellationToken` 与 `tree_node` 模块交互，以管理取消状态。
*   `WaitForCancellationFuture` 和 `WaitForCancellationFutureOwned` 使用 `CancellationToken` 来确定何时完成。
*   `DropGuard` 使用 `CancellationToken` 在其被丢弃时取消令牌。
