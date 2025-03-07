这个文件定义了一个名为 `PollSender` 的结构体，它是一个 `tokio::sync::mpsc::Sender` 的包装器，允许在轮询环境中发送消息。它实现了 `futures_sink::Sink` trait，使得 `PollSender` 可以与异步流和接收器一起使用。

**关键组件：**

*   **`PollSendError<T>`**:  一个错误类型，表示 `PollSender` 在发送消息时可能发生的错误，例如通道已关闭。
*   **`State<T>`**:  一个枚举，表示 `PollSender` 的内部状态，包括：
    *   `Idle`:  空闲状态，准备发送消息。
    *   `Acquiring`:  正在尝试获取发送许可。
    *   `ReadyToSend`:  已获得发送许可，准备发送消息。
    *   `Closed`:  通道已关闭。
*   **`PollSender<T>`**:  `PollSender` 的核心结构体，包含：
    *   `sender`:  一个 `Option<Sender<T>>`，持有底层的 `tokio::sync::mpsc::Sender`。
    *   `state`:  一个 `State<T>`，表示当前状态。
    *   `acquire`:  一个 `PollSenderFuture<T>`，用于异步获取发送许可。
*   **`PollSenderFuture<T>`**:  一个内部的 Future，用于异步获取发送许可。它封装了 `ReusableBoxFuture`，以避免在每次轮询时都分配新的 Future。
*   **`make_acquire_future<T>`**:  一个异步函数，用于创建获取发送许可的 Future。
*   **`InnerFuture<'a, T>`**:  `ReusableBoxFuture` 的类型别名。

**功能：**

*   **`new(sender: Sender<T>)`**:  创建一个新的 `PollSender`。
*   **`poll_reserve(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), PollSendError<T>>>`**:  尝试为发送消息预留空间。在调用 `send_item` 之前必须先调用此方法，并确保它返回 `Poll::Ready(Ok(()))`。
*   **`send_item(&mut self, value: T) -> Result<(), PollSendError<T>>`**:  发送一个消息。在调用此方法之前，必须成功调用 `poll_reserve`。
*   **`is_closed(&self) -> bool`**:  检查发送器是否已关闭。
*   **`get_ref(&self) -> Option<&Sender<T>>`**:  获取底层 `Sender` 的引用。
*   **`close(&mut self)`**:  关闭发送器。
*   **`abort_send(&mut self) -> bool`**:  中止当前正在进行的发送操作。
*   **`clone(&self) -> PollSender<T>`**:  克隆 `PollSender`。

**与项目的关系：**

这个文件提供了一个可轮询的发送器，用于在异步环境中安全地发送消息。它允许在没有阻塞的情况下发送消息，这对于构建高性能的异步应用程序至关重要。它通过实现 `Sink` trait，使得 `PollSender` 可以与其他异步组件（如流和接收器）无缝集成。
