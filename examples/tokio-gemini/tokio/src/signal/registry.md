这个文件定义了用于管理和分发信号通知的注册表，是 Tokio 信号处理机制的核心部分。它包含以下关键组件：

*   **`EventId`**:  一个 `usize` 类型，用于唯一标识一个事件。
*   **`EventInfo`**:  存储特定事件的状态信息，包括：
    *   `pending`:  一个 `AtomicBool`，指示是否有一个通知待发送。
    *   `tx`:  一个 `watch::Sender<()>`，用于向注册的监听器发送通知。
*   **`Storage`**:  一个 trait，定义了用于存储和访问 `EventInfo` 的接口。它允许不同的存储实现，例如 `Vec<EventInfo>`。
*   **`Registry<S>`**:  核心结构体，用于管理事件注册、记录和广播。它泛型化了存储类型 `S`，并提供了以下方法：
    *   `register_listener(event_id: EventId)`:  为给定的 `event_id` 注册一个新的监听器，并返回一个 `watch::Receiver<()>` 用于接收通知。
    *   `record_event(event_id: EventId)`:  标记给定的 `event_id` 为已发生，但不会立即通知监听器。
    *   `broadcast()`:  将所有已记录的事件通知给相应的监听器。它会检查 `pending` 标志，如果事件已发生，则通过 `watch::Sender` 发送通知。
*   **`Globals`**:  一个结构体，包含操作系统相关的额外数据 (`OsExtraData`) 和一个 `Registry` 实例 (`Registry<OsStorage>`)。它实现了 `Deref` trait，允许直接访问 `OsExtraData` 中的数据。它还提供了与 `Registry` 相同的方法，用于注册监听器、记录事件和广播事件。
*   **`globals()`**:  一个函数，用于获取全局的 `Globals` 实例。它使用 `OnceCell` 来确保只初始化一次。
*   **`Init`**:  一个 trait，用于初始化类型。
*   **测试模块**:  包含一些测试用例，用于验证 `Registry` 的功能，例如注册、记录、广播和处理无效的 `event_id`。
