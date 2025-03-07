这个文件定义了 Tokio 中用于多生产者、单消费者（MPSC）通道的核心组件。它包含了发送端（`Tx`）、接收端（`Rx`）和通道本身（`Chan`）的结构体，以及用于管理通道容量的信号量（`Semaphore`） trait。

**关键组件：**

*   **`Tx<T, S>` (发送端):**
    *   `inner`: 包含对 `Chan` 的 `Arc` 引用，允许多个发送端共享通道。
    *   `new()`: 创建一个新的发送端。
    *   `send(value: T)`: 将值推送到通道中，并唤醒接收端。
    *   `clone()`: 克隆发送端，增加内部 `tx_count`。
    *   `drop()`: 当发送端被丢弃时，减少 `tx_count`。如果 `tx_count` 变为 0，则关闭通道。
    *   `is_closed()`: 检查通道是否关闭。
    *   `closed()`: 异步等待直到通道关闭。
    *   `same_channel()`: 检查两个发送端是否属于同一个通道。
    *   `downgrade()`: 创建一个弱引用，用于在发送端被丢弃时减少计数。
    *   `upgrade()`: 尝试将弱引用升级为强引用。

*   **`Rx<T, S>` (接收端):**
    *   `inner`: 包含对 `Chan` 的 `Arc` 引用。
    *   `new()`: 创建一个新的接收端。
    *   `recv(cx: &mut Context<'_>) -> Poll<Option<T>>`: 异步接收一个值。如果通道为空，则挂起任务。
    *   `recv_many(cx: &mut Context<'_>, buffer: &mut Vec<T>, limit: usize) -> Poll<usize>`: 异步接收多个值到缓冲区。
    *   `try_recv() -> Result<T, TryRecvError>`: 尝试立即接收一个值。
    *   `close()`: 关闭接收端，通知发送端。
    *   `is_closed()`: 检查通道是否关闭。
    *   `is_empty()`: 检查通道是否为空。
    *   `len()`: 返回通道中值的数量。
    *   `drop()`: 当接收端被丢弃时，清空通道中的剩余值。

*   **`Chan<T, S>` (通道):**
    *   `tx`:  `list::Tx<T>`，用于处理发送端的数据推送。
    *   `rx_waker`: `AtomicWaker`，用于唤醒接收端。
    *   `notify_rx_closed`: `Notify`，用于通知接收端已关闭。
    *   `semaphore`: `S`，用于管理通道的容量。
    *   `tx_count`: `AtomicUsize`，跟踪发送端的数量。
    *   `tx_weak_count`: `AtomicUsize`，跟踪弱发送端的数量。
    *   `rx_fields`: `UnsafeCell<RxFields<T>>`，接收端独有的字段，包括接收端列表和关闭状态。
    *   `send(value: T)`: 将值推送到通道中，并唤醒接收端。
    *   `decrement_weak_count()`: 减少弱计数。
    *   `increment_weak_count()`: 增加弱计数。
    *   `strong_count()`: 获取强引用计数。
    *   `weak_count()`: 获取弱引用计数。
    *   `drop()`: 当通道被丢弃时，清空通道中的剩余值。

*   **`Semaphore` (信号量):**
    *   一个 trait，定义了用于控制通道容量的方法。
    *   `is_idle()`: 检查信号量是否空闲。
    *   `add_permit()`: 增加一个许可。
    *   `add_permits()`: 增加多个许可。
    *   `close()`: 关闭信号量。
    *   `is_closed()`: 检查信号量是否关闭。
    *   实现了 `bounded::Semaphore` 和 `unbounded::Semaphore` 两种信号量。

*   **`RxFields<T>`:**
    *   `list`: `list::Rx<T>`，用于处理接收端的数据弹出。
    *   `rx_closed`: `bool`，指示接收端是否已关闭。

*   **`channel<T, S: Semaphore>(semaphore: S) -> (Tx<T, S>, Rx<T, S>)`:**
    *   创建一个新的通道，返回发送端和接收端。

**工作原理：**

1.  **发送：** 发送端将值推送到内部的 `list::Tx` 中，并唤醒接收端。
2.  **接收：** 接收端从 `list::Rx` 中弹出值。如果通道为空，则挂起任务。
3.  **容量控制：** 信号量用于控制通道的容量，例如，在有界通道中限制未读消息的数量。
4.  **关闭：** 当所有发送端被丢弃时，通道关闭。接收端也可以主动关闭通道。

**与其他组件的关联：**

*   `loom`: 用于并发原语的抽象，例如 `AtomicWaker` 和 `AtomicUsize`。
*   `list`:  用于实现无锁队列，存储通道中的消息。
*   `error`: 定义了通道操作可能发生的错误。
*   `util::cacheline`: 用于缓存行填充，以减少伪共享。
*   `runtime::park`: 用于线程的阻塞和唤醒。
