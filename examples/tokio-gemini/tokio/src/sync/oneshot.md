这个文件定义了 `tokio::sync` 模块中的 `oneshot` 通道，用于在异步任务之间发送单个消息。

**主要组成部分：**

*   **`Sender<T>`**:  发送端，用于将类型为 `T` 的值发送到通道。
    *   `send(self, t: T) -> Result<(), T>`:  尝试发送一个值。如果接收端已关闭，则返回 `Err(t)`，否则成功发送。
    *   `closed(&mut self)`:  等待接收端关闭。
    *   `is_closed(&self)`:  检查接收端是否已关闭。
    *   `poll_closed(&mut self, cx: &mut Context<'_>) -> Poll<()>`:  轮询检查接收端是否关闭，并在接收端关闭时唤醒。
*   **`Receiver<T>`**:  接收端，用于从通道接收类型为 `T` 的值。
    *   `close(&mut self)`:  关闭接收端，阻止发送端发送值。
    *   `is_terminated(&self)`:  检查接收端是否已终止（已接收值或发送端已关闭）。
    *   `is_empty(&self)`:  检查通道是否为空（没有值）。
    *   `try_recv(&mut self) -> Result<T, TryRecvError>`:  尝试立即接收一个值。
    *   `blocking_recv(self) -> Result<T, RecvError>`:  阻塞接收值，仅在同步上下文中使用。
*   **`error` 模块**:  定义了 `oneshot` 通道可能产生的错误类型。
    *   `RecvError`:  当发送端被丢弃而没有发送值时，接收端会返回此错误。
    *   `TryRecvError`:  `try_recv` 函数可能返回的错误。包括 `Empty`（通道为空）和 `Closed`（发送端已关闭）。
*   **`Inner<T>`**:  内部结构，包含通道的状态、值、发送端和接收端的任务。
    *   `state`:  原子整数，用于管理通道的状态（例如，是否已发送值、是否已关闭）。
    *   `value`:  `UnsafeCell`，用于存储发送的值。
    *   `tx_task`:  发送端的任务，用于在接收端关闭时唤醒。
    *   `rx_task`:  接收端的任务，用于在值被发送时唤醒。
*   **`Task`**:  包装了 `Waker`，用于任务间的唤醒。
*   **`State`**:  一个结构体，用于表示通道的状态，并提供原子操作来修改状态。
*   **`channel<T>() -> (Sender<T>, Receiver<T>)`**:  创建一个新的 `oneshot` 通道，返回发送端和接收端。

**工作原理：**

1.  **创建通道：**  `channel()` 函数创建一个 `Inner` 结构体，包含状态、值和任务。然后，它创建 `Sender` 和 `Receiver` 实例，并将对 `Inner` 的 `Arc` 引用传递给它们。
2.  **发送值：**  `Sender::send()` 方法将值存储在 `Inner` 的 `value` 字段中，并设置状态为“已发送”。如果接收端已关闭，则发送失败。
3.  **接收值：**  `Receiver` 实现了 `Future` trait。当 `Receiver::poll()` 被调用时，它会检查通道的状态。
    *   如果值已发送，则返回 `Ready(Ok(value))`。
    *   如果发送端已关闭，则返回 `Ready(Err(RecvError))`。
    *   如果值尚未发送，则将当前任务注册为接收任务，并返回 `Pending`。
4.  **关闭通道：**  `Receiver::close()` 方法设置通道状态为“已关闭”，阻止发送端发送值。`Sender` 和 `Receiver` 的 `Drop` 实现会清理资源。

**与其他组件的关系：**

*   `oneshot` 通道是 `tokio::sync` 模块中的一个基本同步原语，用于在异步任务之间传递单个值。
*   它与其他通道（如 `mpsc` 和 `broadcast`）不同，因为它只能发送一个值。
*   它经常用于在任务之间传递结果或信号。
*   它使用 `Future` trait 来实现异步接收。
*   它使用原子操作和 `UnsafeCell` 来安全地共享状态。
