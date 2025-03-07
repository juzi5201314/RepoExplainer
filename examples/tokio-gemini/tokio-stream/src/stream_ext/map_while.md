这段代码定义了一个名为 `MapWhile` 的结构体，它实现了 `Stream` trait。它的主要作用是为 `Stream` 提供一个 `map_while` 方法，该方法允许在满足特定条件时对流中的元素进行转换。

**关键组件：**

*   **`MapWhile<St, F>` 结构体:**
    *   `stream: St`：被包装的原始 `Stream`。`#[pin]` 属性表示该字段需要被固定（pinned），以确保在异步操作期间其内存地址不会改变。
    *   `f: F`：一个闭包或函数，用于将原始流中的元素转换为新的类型。该闭包接受原始流的元素作为输入，并返回一个 `Option<T>`。如果闭包返回 `Some(T)`，则将 `T` 作为新流的元素；如果返回 `None`，则停止迭代并结束流。
*   **`pin_project!` 宏:**  用于安全地处理被固定的字段。它生成必要的代码，以确保在 `MapWhile` 结构体中对 `stream` 字段进行投影时，不会违反 Rust 的借用规则。
*   **`Stream` trait 的实现:**
    *   `type Item = T;`：定义了新流的元素类型。
    *   `poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<T>>`：这是 `Stream` trait 的核心方法。它从底层流中获取下一个元素，并使用闭包 `f` 对其进行转换。如果底层流返回 `Some(item)`，则闭包 `f` 被调用，并将结果包装在 `Poll::Ready(Some(T))` 中返回。如果闭包返回 `None`，则返回 `Poll::Ready(None)`，表示流结束。如果底层流返回 `Poll::Pending`，则 `poll_next` 也返回 `Poll::Pending`。
    *   `size_hint(&self) -> (usize, Option<usize>)`：提供关于流大小的提示。由于 `map_while` 可能会提前结束流，因此下限为 0，上限与底层流的上限相同。
*   **`new(stream: St, f: F)` 方法:**  一个构造函数，用于创建 `MapWhile` 实例。

**工作原理：**

`MapWhile` 结构体包装了一个底层的 `Stream` 和一个转换函数 `f`。当调用 `poll_next` 时，它会从底层流中获取下一个元素。然后，它将该元素传递给转换函数 `f`。如果 `f` 返回 `Some(T)`，则将 `T` 作为新流的元素返回。如果 `f` 返回 `None`，则表示应该停止迭代，并返回 `Poll::Ready(None)`，从而结束流。

**与项目的关系：**
