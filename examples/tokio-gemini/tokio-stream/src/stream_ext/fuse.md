这段代码定义了 `Fuse` 结构体，它实现了 `Stream` trait，用于包装另一个 `Stream`，并确保在原始 `Stream` 结束之后，`Fuse` 永远不会再次产生任何值。这类似于一个“熔断器”，一旦底层流结束，`Fuse` 就会停止产生任何输出。

**关键组件：**

*   **`Fuse<T>` 结构体:**
    *   这是一个泛型结构体，包装了一个 `Option<T>` 类型的 `stream` 字段。`stream` 字段使用 `#[pin]` 属性，这意味着它可以在内存中被固定，这对于异步编程至关重要。
    *   `stream` 字段持有原始的 `Stream`，使用 `Option` 包裹，是为了在原始 `Stream` 结束时将其设置为 `None`，从而防止后续的轮询。
*   **`new(stream: T)` 方法:**
    *   这是一个构造函数，用于创建一个 `Fuse` 实例，将给定的 `Stream` 包装起来。
*   **`poll_next` 方法 (实现 `Stream` trait):**
    *   这是 `Fuse` 的核心逻辑。它尝试从内部的 `stream` 中获取下一个值。
    *   首先，它使用 `Option::as_pin_mut` 将 `stream` 转换为可变引用的 `Pin`，以便安全地调用其 `poll_next` 方法。
    *   如果 `stream` 存在 (即 `Some(stream)`)，则调用底层 `stream` 的 `poll_next` 方法。
    *   如果底层 `stream` 返回 `Poll::Ready(Some(item))`，则 `Fuse` 也会返回 `Poll::Ready(Some(item))`.
    *   如果底层 `stream` 返回 `Poll::Ready(None)`，这意味着底层 `stream` 已经结束。此时，`Fuse` 会将内部的 `stream` 设置为 `None`，以防止后续的轮询。
    *   如果 `stream` 不存在 (即 `None`)，则直接返回 `Poll::Ready(None)`，表示 `Fuse` 已经结束。
*   **`size_hint` 方法 (实现 `Stream` trait):**
    *   返回底层 `stream` 的大小提示。如果 `stream` 已经结束，则返回 `(0, Some(0))`。

**如何融入项目：**

`Fuse` 结构体通常与 `StreamExt` trait 一起使用。`StreamExt` 提供了 `fuse()` 方法，该方法用于将一个 `Stream` 转换为 `Fuse<T>`。这允许开发者确保一个流在第一次结束之后，不会再产生任何值，这在某些情况下非常有用，例如，当需要确保一个流只被处理一次时。
