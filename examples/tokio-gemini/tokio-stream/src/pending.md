这个文件定义了一个名为 `Pending` 的结构体，它实现了一个永远不会准备好的流。

**主要组成部分：**

*   **`Pending<T>` 结构体:**
    *   这是一个泛型结构体，使用 `PhantomData<T>` 来持有类型 `T`。`PhantomData` 是一种零大小的类型，用于告诉编译器类型 `T` 被结构体使用，即使结构体本身不直接存储 `T` 的值。
    *   `#[derive(Debug)]` 允许使用 `{:?}` 格式化打印调试信息。
    *   `#[must_use = "streams do nothing unless polled"]` 属性是一个警告，提醒用户流只有在被轮询时才会执行操作，如果创建了流但没有使用它，编译器会发出警告。
    *   `impl<T> Unpin for Pending<T> {}`、`unsafe impl<T> Send for Pending<T> {}` 和 `unsafe impl<T> Sync for Pending<T> {}` 分别实现了 `Unpin`、`Send` 和 `Sync` trait，允许 `Pending` 在多线程环境中使用，并且可以安全地移动。
*   **`pending<T>()` 函数:**
    *   这是一个常量函数，用于创建一个 `Pending` 类型的流。
    *   它返回一个 `Pending<T>` 实例，该实例使用 `PhantomData` 来持有类型 `T`。
*   **`impl<T> Stream for Pending<T>`:**
    *   这为 `Pending<T>` 结构体实现了 `Stream` trait。
    *   `type Item = T;` 定义了流的项类型为 `T`。
    *   `fn poll_next(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<Option<T>>`：这是 `Stream` trait 的核心方法，用于尝试从流中获取下一个值。在这个实现中，它总是返回 `Poll::Pending`，这意味着流永远不会准备好产生任何值。
    *   `fn size_hint(&self) -> (usize, Option<usize>)`：提供流的大小提示。这里返回 `(0, None)`，表示流的已知最小大小为 0，但没有最大大小的限制。

**功能和作用：**

`Pending` 流的主要作用是创建一个永远不会产生任何值的流。这在以下场景中非常有用：

*   **测试:** 在测试异步代码时，可以使用 `pending` 流来模拟一个永远不会完成的操作。
*   **占位符:** 当需要一个流，但暂时没有可用的数据源时，可以使用 `pending` 流作为占位符。
*   **控制流:** 可以使用 `pending` 流来控制异步操作的流程，例如，在某些条件下阻止流的执行。
