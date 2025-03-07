这个文件定义了 `Then` 结构体，它实现了 `Stream` trait，用于实现 `StreamExt::then` 方法。`then` 方法允许对流中的每个元素应用一个异步操作（Future），并将结果作为新的流输出。

**关键组件：**

*   **`Then<St, Fut, F>` 结构体：**
    *   `stream: St`：被包装的原始流，类型为 `Stream`。
    *   `future: Option<Fut>`：一个可选的 `Future`，用于执行对流元素的异步操作。在处理一个元素时，会创建一个 `Future`，并将其存储在这里。
    *   `f: F`：一个闭包或函数，它接受原始流的元素作为输入，并返回一个 `Future`。这个 `Future` 定义了对每个元素的异步操作。
*   **`pin_project!` 宏：** 用于安全地将结构体中的字段固定（pinning），确保在异步操作期间字段的内存地址不会改变。
*   **`Stream` trait 的实现：**
    *   `type Item = Fut::Output;`：定义了新流的输出类型，即 `Future` 的输出类型。
    *   `poll_next` 方法：
        *   首先检查 `future` 是否存在。如果存在，则轮询该 `Future`。如果 `Future` 完成，则将其结果作为新流的下一个元素返回。
        *   如果 `future` 不存在，则轮询原始流 `stream`。如果原始流产生一个元素，则使用闭包 `f` 创建一个 `Future`，并将该 `Future` 存储在 `future` 字段中。
        *   如果原始流结束，则新流也结束。
    *   `size_hint` 方法：提供关于流大小的提示。

**工作流程：**

1.  `StreamExt::then` 方法创建一个 `Then` 结构体的实例，将原始流和处理函数（闭包）封装起来。
2.  当调用 `Then` 结构体的 `poll_next` 方法时：
    *   如果当前没有正在执行的 `Future`，则从原始流中获取一个元素。
    *   使用闭包处理该元素，生成一个 `Future`。
    *   将该 `Future` 存储在 `future` 字段中。
    *   轮询 `future`，直到它完成。
    *   返回 `Future` 的结果作为新流的下一个元素。
    *   如果原始流已经结束，则新流也结束。

**与其他文件的关系：**

*   `StreamExt` trait：`then` 方法是 `StreamExt` trait 的一个扩展方法，该 trait 提供了对 `Stream` 的额外功能。
*   `Stream` trait：`Then` 结构体实现了 `Stream` trait，从而能够作为流使用。
*   `Future` trait：`then` 方法使用 `Future` 来执行异步操作。
