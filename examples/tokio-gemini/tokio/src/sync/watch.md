这个文件定义了 `tokio::sync::watch` 模块，它实现了一个多生产者、多消费者通道，该通道仅保留最后发送的值。这对于从代码库中的多个点监视值的变化（例如配置值的变化）非常有用。

**主要组件：**

*   **`Sender<T>`**: 发送端，用于向通道发送值。
    *   `send(value: T)`: 发送一个新值，通知所有接收者。如果通道已关闭（所有接收者都已丢弃），则发送失败。
    *   `send_modify(modify: F)`: 在原地修改被监视的值，并通知所有接收者。
    *   `send_if_modified(modify: F)`: 有条件地在原地修改被监视的值，仅当修改时通知所有接收者。
    *   `send_replace(value: T)`: 发送一个新值，通知所有接收者，并返回通道中的先前值。
    *   `borrow()`: 返回对最近发送值的引用。
    *   `is_closed()`: 检查通道是否已关闭（所有接收者都已丢弃）。
    *   `closed()`: 当所有接收者都已丢弃时完成。
    *   `subscribe()`: 创建一个新的 `Receiver`，连接到此 `Sender`。
    *   `receiver_count()`: 返回当前存在的接收者数量。
    *   `sender_count()`: 返回当前存在的发送者数量。
    *   `same_channel(other: &Self)`: 如果发送者属于同一通道，则返回 `true`。
*   **`Receiver<T>`**: 接收端，用于从通道接收值。
    *   `borrow()`: 返回对最近发送值的引用，但不标记为已查看。
    *   `borrow_and_update()`: 返回对最近发送值的引用，并标记为已查看。
    *   `has_changed()`: 检查此通道是否包含此接收者尚未查看的消息。
    *   `mark_changed()`: 将状态标记为已更改。
    *   `mark_unchanged()`: 将状态标记为未更改。
    *   `changed()`: 等待更改通知，然后将最新值标记为已查看。
    *   `wait_for(f: impl FnMut(&T) -> bool)`: 等待满足提供的条件的某个值。
    *   `same_channel(other: &Self)`: 如果接收者属于同一通道，则返回 `true`。
*   **`channel<T>(init: T)`**: 创建一个新的 watch 通道，返回发送和接收句柄。
*   **`Ref<'a, T>`**: 对通道中值的只读引用。
    *   `has_changed()`: 指示自上次标记为已查看以来，借用的值是否被视为已更改。
*   **`Shared<T>`**: 包含通道的共享状态，包括值、版本、引用计数和通知机制。
*   **`error` 模块**: 定义了 `SendError` 和 `RecvError` 错误类型。
*   **`state` 模块**: 定义了用于管理通道状态的原子类型和版本。
*   **`big_notify` 模块**: 优化通知机制，以减少争用。

**工作原理：**

1.  `channel` 函数创建一个 `Shared` 结构体，该结构体包含实际的值（使用 `RwLock` 保护）、状态（使用 `AtomicState` 跟踪版本和关闭状态）、引用计数和通知机制。
2.  `Sender` 和 `Receiver` 拥有 `Shared` 结构的 `Arc` 引用，允许它们共享状态。
3.  当 `Sender` 调用 `send` 时，它会获取 `RwLock` 的写锁，更新值，增加版本号，并通知所有 `Receiver`。
4.  `Receiver` 可以通过 `borrow` 获取当前值（读锁），或者通过 `borrow_and_update` 获取当前值并标记为已查看。
5.  `Receiver` 的 `changed` 方法会等待，直到版本号发生变化（即有新值发送），或者 `Sender` 被丢弃。
6.  `Receiver` 的 `has_changed` 方法检查当前版本号是否与上次查看的版本号不同。

**与其他组件的关系：**

*   `tokio::sync::notify`: 用于通知等待的接收者。
*   `tokio::task::coop`: 用于在 `changed` 和 `wait_for` 方法中进行协作调度。
*   `tokio::loom`: 用于在测试中模拟并发行为。
