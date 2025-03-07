这个文件定义了一个关闭通道，用于在 Tokio 运行时中优雅地关闭阻塞线程池。

**主要组成部分：**

*   **`Sender` 结构体:**
    *   持有 `oneshot::Sender<()>` 的 `Arc` 引用。每个工作线程都持有一个 `Sender` 实例。
    *   当所有 `Sender` 实例被丢弃时，`Receiver` 会收到通知。
*   **`Receiver` 结构体:**
    *   持有 `oneshot::Receiver<()>`。
    *   用于接收关闭信号。
*   **`channel()` 函数:**
    *   创建一个 `oneshot` 通道。
    *   创建一个 `Sender` 和一个 `Receiver` 实例，并将 `oneshot` 通道的发送端和接收端分别赋给它们。
    *   返回 `(Sender, Receiver)` 元组。
*   **`Receiver::wait()` 方法:**
    *   阻塞当前线程，直到所有 `Sender` 句柄被丢弃。
    *   可选地，可以设置一个超时时间。
        *   如果 `timeout` 为 `Some(Duration)`，则线程最多阻塞 `timeout` 时长。
        *   如果 `timeout` 为 `None`，则线程无限期地阻塞，直到收到关闭信号。
    *   如果超时已过，则返回 `false`；否则返回 `true`。
    *   在阻塞之前，会尝试进入阻塞区域，以确保当前线程可以安全地阻塞。
    *   如果阻塞失败，则会 panic。

**工作原理：**

1.  当 Tokio 运行时启动时，会创建一个关闭通道。
2.  每个工作线程都会持有 `Sender` 实例。
3.  当运行时需要关闭时，会丢弃所有 `Sender` 实例。
4.  当所有 `Sender` 实例都被丢弃时，`oneshot` 通道的发送端被关闭，`Receiver` 接收到信号。
5.  `Receiver::wait()` 方法会阻塞当前线程，直到收到关闭信号。
6.  当 `Receiver` 收到关闭信号时，`wait()` 方法返回，线程可以安全地退出。

**与其他组件的关联：**

*   `BlockingPool`:  `BlockingPool` 使用这个关闭通道来优雅地关闭其内部的阻塞线程。
*   `tokio::runtime`:  这个文件是 Tokio 运行时的一部分，用于管理阻塞线程池的关闭。
