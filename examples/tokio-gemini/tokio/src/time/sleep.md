这个文件定义了 Tokio 运行时中用于实现休眠功能的关键组件。它提供了 `sleep_until` 和 `sleep` 这两个公共函数，以及 `Sleep` 结构体，用于创建和管理休眠的 Future。

**主要组件：**

1.  **`sleep_until(deadline: Instant) -> Sleep`**:
    *   此函数创建一个 `Sleep` Future，该 Future 将等待直到指定的 `deadline`（一个 `Instant` 类型，表示一个时间点）到达。
    *   它使用 `trace::caller_location()` 获取调用者的位置信息，用于调试和跟踪。
    *   它调用 `Sleep::new_timeout` 来创建 `Sleep` 实例。

2.  **`sleep(duration: Duration) -> Sleep`**:
    *   此函数创建一个 `Sleep` Future，该 Future 将等待指定的 `duration`（一个 `Duration` 类型，表示一个时间段）过去。
    *   它通过将当前时间 `Instant::now()` 与 `duration` 相加来计算截止时间，然后调用 `sleep_until`。
    *   如果计算截止时间时发生溢出，则使用一个非常远的未来时间点作为截止时间。

3.  **`Sleep` 结构体**:
    *   这是一个 `Future`，由 `sleep_until` 和 `sleep` 函数返回。
    *   它使用 `pin_project_lite` 宏来确保 `Sleep` 结构体可以被安全地 `Pin` 住。
    *   `inner`: 包含用于跟踪的上下文信息，在启用跟踪时使用。
    *   `entry`:  一个 `TimerEntry` 实例，它负责与 Tokio 的时间轮交互，管理休眠的实际时间。
    *   `new_timeout(deadline: Instant, location: Option<&'static Location<'static>>) -> Sleep`:  创建一个新的 `Sleep` 实例。它获取当前的调度器句柄，创建一个 `TimerEntry`，并将截止时间传递给它。
    *   `far_future(location: Option<&'static Location<'static>>) -> Sleep`: 创建一个截止时间为遥远未来的 `Sleep` 实例。
    *   `deadline(&self) -> Instant`:  返回 `Sleep` Future 的截止时间。
    *   `is_elapsed(&self) -> bool`:  检查 `Sleep` Future 是否已经超时。
    *   `reset(self: Pin<&mut Self>, deadline: Instant)`:  重置 `Sleep` Future 的截止时间。这允许在不创建新 Future 的情况下更改休眠时间。
    *   `reset_without_reregister(self: Pin<&mut Self>, deadline: Instant)`: 重置 `Sleep` Future 的截止时间，但不重新注册它以被唤醒。
    *   `poll(mut self: Pin<&mut Self>, cx: &mut task::Context<'_>) -> Poll<Self::Output>`:  实现 `Future` trait 的 `poll` 方法。它调用 `entry.poll_elapsed()` 来检查时间是否已到。如果时间已到，则返回 `Poll::Ready(())`，否则返回 `Poll::Pending`。

**功能和作用：**

*   **休眠功能**:  `sleep` 和 `sleep_until` 函数提供了在 Tokio 运行时中进行异步休眠的能力，类似于标准库中的 `std::thread::sleep`，但不会阻塞线程。
*   **时间管理**:  `Sleep` 结构体与 Tokio 的时间轮集成，用于在指定的时间点唤醒任务。
*   **取消**:  通过丢弃 `Sleep` Future 来取消休眠。
*   **重置**:  `reset` 方法允许在不创建新 Future 的情况下更改休眠时间，这对于需要动态调整休眠时间的场景非常有用。
*   **错误处理**:  `poll` 方法中的错误处理，如果发生错误，则会 panic。
