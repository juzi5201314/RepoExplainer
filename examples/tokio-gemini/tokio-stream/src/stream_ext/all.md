这个文件定义了 `AllFuture` 结构体，它实现了 `StreamExt` trait 中的 `all` 方法。`all` 方法用于判断一个流中的所有元素是否都满足给定的条件。

**关键组件：**

*   **`AllFuture<'a, St: ?Sized, F>` 结构体:**
    *   `stream: &'a mut St`:  对流的引用，用于从中获取元素。
    *   `f: F`:  一个闭包或函数，用于判断流中的每个元素是否满足条件。它接受流的元素作为输入，并返回一个布尔值。
    *   `_pin: PhantomPinned`:  一个 `PhantomPinned` 字段，用于确保 `AllFuture` 不可移动，这对于与异步 trait 方法的兼容性很重要。
*   **`new(stream: &'a mut St, f: F) -> Self` 方法:**  一个构造函数，用于创建 `AllFuture` 实例。
*   **`impl<St, F> Future for AllFuture<'_, St, F>`:**  为 `AllFuture` 结构体实现 `Future` trait。
    *   `type Output = bool`:  `Future` 的输出类型，表示流中的所有元素是否都满足条件。
    *   `poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>`:  `Future` 的 `poll` 方法，用于驱动 `Future` 的执行。
        *   它从流中获取元素，并使用提供的闭包 `f` 来判断每个元素是否满足条件。
        *   如果任何元素不满足条件，则立即返回 `Poll::Ready(false)`。
        *   如果流耗尽（即没有更多元素），则返回 `Poll::Ready(true)`。
        *   为了避免在单个 `poll` 调用中消耗过多的 CPU 时间，它会限制每次迭代从流中获取的元素数量（最多 32 个）。
        *   如果流没有准备好产生更多元素，则会调用 `cx.waker().wake_by_ref()` 来唤醒任务，并返回 `Poll::Pending`。

**与项目的关系：**

这个文件是 `tokio-stream` crate 的一部分，它扩展了 `Stream` trait，提供了额外的功能。`AllFuture` 结构体是 `StreamExt` trait 中 `all` 方法的实现，用于判断流中所有元素是否满足特定条件。它允许用户以异步方式处理流，并在所有元素都满足条件时得到一个布尔结果。
