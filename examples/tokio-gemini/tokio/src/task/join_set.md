这个文件定义了 `JoinSet` 结构体，它是一个 Tokio 运行时中任务的集合。`JoinSet` 允许异步等待这些任务的完成，并以它们完成的顺序返回结果。

**主要组件：**

*   **`JoinSet<T>`**:  `JoinSet` 是一个泛型结构体，用于存储和管理由 Tokio 运行时生成的任务。所有任务必须具有相同的返回类型 `T`。
    *   `inner: IdleNotifiedSet<JoinHandle<T>>`：内部使用 `IdleNotifiedSet` 来存储 `JoinHandle`。`IdleNotifiedSet` 是一种数据结构，用于跟踪任务的状态，并允许在任务完成时进行通知。
*   **`Builder<'a, T>`**:  一个构建器，用于在 `JoinSet` 上配置和生成任务。它允许设置任务的名称（如果启用了 tracing 功能）。
*   **`JoinHandle<T>`**:  表示一个已生成的任务，可以用来等待任务完成或取消任务。
*   **`AbortHandle`**:  用于远程取消任务的句柄。
*   **`JoinError`**:  一个枚举，表示任务可能发生的错误，例如任务被取消或发生了 panic。

**功能：**

*   **创建和管理任务：**
    *   `new()`: 创建一个新的 `JoinSet`。
    *   `len()`: 返回 `JoinSet` 中当前任务的数量。
    *   `is_empty()`: 检查 `JoinSet` 是否为空。
    *   `build_task()`: (如果启用了 tracing) 返回一个 `Builder`，用于配置任务。
    *   `spawn(task)`: 在默认 Tokio 运行时上生成一个任务，并将其添加到 `JoinSet` 中。
    *   `spawn_on(task, handle)`: 在指定的 Tokio 运行时句柄上生成一个任务，并将其添加到 `JoinSet` 中。
    *   `spawn_local(task)`: 在当前的 `LocalSet` 上生成一个任务，并将其添加到 `JoinSet` 中。
    *   `spawn_local_on(task, local_set)`: 在指定的 `LocalSet` 上生成一个任务，并将其添加到 `JoinSet` 中。
    *   `spawn_blocking(f)`: 在阻塞线程池上生成一个阻塞任务，并将其添加到 `JoinSet` 中。
    *   `spawn_blocking_on(f, handle)`: 在指定运行时句柄的阻塞线程池上生成一个阻塞任务，并将其添加到 `JoinSet` 中。
*   **等待任务完成：**
    *   `join_next()`: 异步等待 `JoinSet` 中下一个完成的任务，并返回其结果。
    *   `join_next_with_id()`: 异步等待 `JoinSet` 中下一个完成的任务，并返回其结果和任务 ID。
    *   `try_join_next()`: 尝试获取已完成的任务的结果，如果没有任何任务完成，则立即返回 `None`。
    *   `try_join_next_with_id()`: 尝试获取已完成的任务的结果和任务 ID，如果没有任何任务完成，则立即返回 `None`。
    *   `join_all()`: 等待 `JoinSet` 中所有任务完成，并返回一个包含所有结果的向量。如果任何任务 panic，则会 panic。
*   **控制任务：**
    *   `abort_all()`: 取消 `JoinSet` 中的所有任务。
    *   `shutdown()`: 取消所有任务并等待它们完成。
    *   `detach_all()`: 从 `JoinSet` 中移除所有任务，但不会取消它们。
*   **轮询任务：**
    *   `poll_join_next()`: 轮询 `JoinSet` 中是否有任务完成。
    *   `poll_join_next_with_id()`: 轮询 `JoinSet` 中是否有任务完成，并返回任务 ID。

**与其他部分的关联：**

*   `JoinSet` 依赖于 Tokio 运行时，用于生成和管理任务。
*   `JoinSet` 使用 `JoinHandle` 和 `AbortHandle` 来控制和等待任务。
*   `JoinSet` 使用 `IdleNotifiedSet` 来高效地管理任务状态和通知。
*   `JoinSet` 实现了 `FromIterator` trait，允许从一个迭代器创建 `JoinSet`。
