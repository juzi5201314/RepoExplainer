这个文件定义了 `JoinHandle` 结构体，它代表了对 Tokio 任务的拥有权限，可以等待任务的终止。 类似于 `std::thread::JoinHandle`，但适用于 Tokio 任务而不是线程。

**关键组件：**

*   **`JoinHandle<T>`**:  一个结构体，用于等待 Tokio 任务的完成。 `T` 是任务的返回值类型。
    *   `raw: RawTask`:  一个底层的 `RawTask` 结构体，用于与任务的底层表示交互。
    *   `_p: PhantomData<T>`:  一个 PhantomData，用于标记 `JoinHandle` 拥有任务的返回值类型 `T`。
*   **`new(raw: RawTask) -> JoinHandle<T>`**:  创建一个新的 `JoinHandle` 实例。
*   **`abort(&self)`**:  取消与句柄关联的任务。  如果任务尚未开始，则可能阻止其启动。  `spawn_blocking` 任务无法被取消。
*   **`is_finished(&self) -> bool`**:  检查与此 `JoinHandle` 关联的任务是否已完成。
*   **`set_join_waker(&mut self, waker: &Waker)`**:  设置在任务完成时被通知的唤醒器。
*   **`abort_handle(&self) -> super::AbortHandle`**:  返回一个 `AbortHandle`，可用于远程中止此任务。
*   **`id(&self) -> super::Id`**:  返回一个任务 ID，该 ID 唯一标识此任务。
*   **`Future for JoinHandle<T>`**:  实现了 `Future` trait，允许使用 `await` 等待任务完成并获取其结果。  `poll` 方法尝试读取任务的输出，如果任务未完成，则存储唤醒器并在任务完成时通知它。
*   **`Drop for JoinHandle<T>`**:  当 `JoinHandle` 被丢弃时，如果任务尚未完成，则会尝试快速或慢速地处理任务的清理。
*   **`fmt::Debug for JoinHandle<T>`**:  实现了 `Debug` trait，允许以调试格式打印 `JoinHandle` 的信息。

**与其他部分的关联：**

*   与 `task::spawn` 和 `task::spawn_blocking` 函数一起使用，用于创建和管理 Tokio 任务。
*   与 `JoinError` 结合使用，用于处理任务的错误，包括取消和 panic。
*   与 `AbortHandle` 结合使用，用于远程中止任务。
*   使用 `RawTask` 与 Tokio 运行时中的底层任务表示交互。
