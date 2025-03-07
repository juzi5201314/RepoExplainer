这个文件定义了一个 `StreamMock`，它是一个模拟 `Stream` 特征的结构体，用于测试与流交互的代码。

**主要组件：**

*   **`Action<T>` 枚举：** 定义了 `StreamMock` 可以执行的两种操作：
    *   `Next(T)`：产生一个类型为 `T` 的值。
    *   `Wait(Duration)`：等待一段时间。
*   **`StreamMockBuilder<T>` 结构体：**  一个构建器，用于创建 `StreamMock` 实例。它允许通过 `next()` 和 `wait()` 方法添加操作到内部的 `actions` 队列中。
    *   `new()`：创建一个新的空的构建器。
    *   `next(value: T)`：将一个值添加到流中，表示流将产生这个值。
    *   `wait(duration: Duration)`：将一个等待操作添加到流中，表示流将暂停一段时间。
    *   `build()`：根据构建器中的操作队列创建一个 `StreamMock` 实例。
*   **`StreamMock<T>` 结构体：**  实现了 `Stream` 特征的模拟流。
    *   `actions: VecDeque<Action<T>>`：一个双端队列，存储了要执行的操作。
    *   `sleep: Option<Pin<Box<Sleep>>>`：一个可选的 `Sleep` future，用于处理 `Wait` 操作。
    *   `poll_next()`：实现了 `Stream` 特征的 `poll_next` 方法，用于从流中获取下一个值。它会根据 `actions` 队列中的操作来产生值或等待。
    *   `next_action()`：从 `actions` 队列中弹出一个操作。
    *   `Drop` trait 的实现：在 `StreamMock` 被丢弃时，检查是否所有操作都已被消费，如果未消费，则会 panic，帮助开发者发现测试中的问题。

**工作原理：**

1.  使用 `StreamMockBuilder` 构建一个 `StreamMock` 实例，通过 `next()` 和 `wait()` 方法定义流的行为。
2.  当调用 `poll_next()` 方法时，`StreamMock` 会从 `actions` 队列中取出操作。
3.  如果操作是 `Next(item)`，则返回 `Poll::Ready(Some(item))`，表示产生一个值。
4.  如果操作是 `Wait(duration)`，则创建一个 `Sleep` future，并将 `poll_next()` 的状态设置为 `Poll::Pending`，表示流正在等待。当 `Sleep` future 完成时，`poll_next()` 将再次被调用，并从 `actions` 队列中取出下一个操作。
5.  当 `actions` 队列为空时，`poll_next()` 返回 `Poll::Ready(None)`，表示流结束。

**与其他部分的关联：**

这个文件定义了一个用于测试的模拟流，它允许开发者模拟流的行为，例如产生特定的值或等待一段时间。这对于测试依赖于流的代码非常有用，因为它允许开发者控制流的行为，并验证代码是否按预期工作。
