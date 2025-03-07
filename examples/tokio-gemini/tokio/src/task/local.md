这个文件 `tokio/src/task/local.rs` 实现了 `tokio` 运行时中用于在当前线程上运行 `!Send` futures 的 `LocalSet` 类型。`LocalSet` 允许开发者在同一个线程上调度和运行那些由于没有实现 `Send` trait 而不能安全地跨线程发送的 futures。

主要组成部分：

*   **`LocalSet` 结构体**:  `LocalSet` 是核心结构体，它管理着一个本地任务集合。它包含一个 `tick` 计数器，用于调度任务；一个 `Context` 结构体的 `Rc` 引用，用于存储线程本地状态；以及一个 `PhantomData` 标记，确保 `LocalSet` 不可 `Send`。
*   **`Context` 结构体**:  `Context` 存储了线程本地状态，包括一个 `Shared` 结构体的 `Arc` 引用，用于在线程间共享状态；以及一个 `unhandled_panic` 标志，用于处理未处理的任务 panic。
*   **`Shared` 结构体**:  `Shared` 存储了 `LocalSet` 在线程间共享的状态，包括一个 `LocalState` 结构体，用于存储本地状态；一个 `Mutex` 保护的远程运行队列；一个 `AtomicWaker`，用于唤醒 `LocalSet` 任务；以及一个配置，用于处理未处理的任务 panic。
*   **`LocalState` 结构体**:  `LocalState` 存储了 `LocalSet` 的本地状态，只能从拥有 `LocalSet` 的线程访问。它包含拥有 `LocalSet` 的线程的 `ThreadId`，一个 `UnsafeCell` 包装的本地运行队列，以及一个 `LocalOwnedTasks` 集合，用于跟踪所有在该执行器上生成的活动任务。
*   **`RunUntil` 结构体**:  一个辅助结构体，用于在 `LocalSet` 上运行一个 future 直到完成。
*   **`CURRENT` 线程局部变量**:  一个线程局部变量，用于存储当前线程的 `LocalData`，`LocalData` 包含 `Context` 的 `RcCell` 和一个 `wake_on_schedule` 标志。
*   **`LocalData` 结构体**:  存储线程本地的上下文信息，包括 `Context` 和 `wake_on_schedule` 标志。
*   **`LocalEnterGuard` 结构体**:  一个用于进入 `LocalSet` 上下文的 guard，它在进入和退出上下文时管理线程局部变量。
*   **`spawn_local` 函数**:  用于在当前 `LocalSet` 或 `LocalRuntime` 上生成一个 `!Send` future。
*   **`spawn_local_inner` 函数**:  `spawn_local` 的内部实现，处理 future 的生成。
*   **`INITIAL_CAPACITY`, `MAX_TASKS_PER_TICK`, `REMOTE_FIRST_INTERVAL` 常量**:  用于配置任务队列和调度行为的常量。

该文件定义了 `LocalSet` 的核心功能，包括：

*   创建 `LocalSet`。
*   进入 `LocalSet` 的上下文。
*   在 `LocalSet` 上生成 `!Send` 任务。
*   运行一个 future 直到完成，同时驱动 `LocalSet` 中的任务。
*   调度和执行任务。
*   处理任务 panic。
*   在 `LocalSet` 销毁时清理资源。
