这个文件定义了 `FilterMap` 结构体，它是 `tokio-stream` 库中 `StreamExt` trait 的 `filter_map` 方法返回的流。`filter_map` 方法用于对流中的每个元素应用一个函数，如果函数返回 `Some(T)`，则将 `T` 包含在新的流中；如果函数返回 `None`，则过滤掉该元素。

**关键组件：**

*   **`FilterMap<St, F>` 结构体：**
    *   `St`：被包装的原始流，实现 `Stream` trait。
    *   `F`：一个闭包或函数，接受原始流的元素类型 `St::Item` 作为输入，并返回 `Option<T>`。
    *   `#[pin]`：使用 `pin_project_lite` 宏来确保 `stream` 字段在内存中是固定的，这对于异步编程至关重要。
*   **`new(stream: St, f: F) -> Self` 方法：**
    *   一个构造函数，用于创建 `FilterMap` 实例。它接收原始流 `stream` 和过滤函数 `f` 作为参数。
*   **`Stream` trait 的实现：**
    *   `type Item = T;`：定义了新流的元素类型，即过滤函数返回的 `Some(T)` 中的 `T`。
    *   `poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<T>>`：核心方法，用于从流中获取下一个元素。
        *   它循环调用原始流的 `poll_next` 方法。
        *   对于原始流返回的每个元素，它应用过滤函数 `f`。
        *   如果过滤函数返回 `Some(e)`，则将 `e` 作为新流的下一个元素返回。
        *   如果过滤函数返回 `None`，则跳过该元素。
        *   如果原始流返回 `None`，则新流也返回 `None`，表示流结束。
    *   `size_hint(&self) -> (usize, Option<usize>)`：提供关于流大小的提示。由于过滤操作可能会过滤掉一些元素，因此下限为 0，上限与原始流的上限相同。
*   **`fmt::Debug` trait 的实现：**
    *   允许对 `FilterMap` 结构体进行调试打印。

**与项目的关系：**

这个文件是 `tokio-stream` 库的一部分，它扩展了 `Stream` trait，提供了 `filter_map` 方法，该方法允许用户根据自定义的过滤逻辑从流中选择元素，并将其映射到新的类型。`FilterMap` 结构体是 `filter_map` 方法的实现，负责处理流的过滤和转换逻辑。
