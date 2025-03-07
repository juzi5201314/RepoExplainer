这段代码定义了一个名为 `Peekable` 的结构体，它实现了 `Stream` trait，并提供了 `peek` 方法，允许用户查看流中的下一个元素，而不会将其从流中移除。

**代码组成部分：**

1.  **引入模块：**
    *   `std::pin::Pin`: 用于处理自引用结构体，确保数据在内存中的位置不会改变。
    *   `std::task::{Context, Poll}`: 用于异步任务的上下文和轮询机制。
    *   `futures_core::Stream`: 定义了异步流的 trait。
    *   `pin_project_lite::pin_project`: 一个宏，用于简化 `Pin` 相关的代码，特别是处理结构体字段的 `Pin` 投影。
    *   `crate::stream_ext::Fuse`:  一个 `Fuse` 结构体，用于将流转换为在完成后不会再次产生值的流。
    *   `crate::StreamExt`:  定义了 `Stream` 的扩展方法，包括 `peekable`。

2.  **`Peekable` 结构体：**
    *   `peek: Option<T::Item>`:  一个 `Option`，用于存储被“peek”的元素。如果为 `Some(item)`，则表示已经 peek 了一个元素，并且该元素尚未被 `next` 消费。如果为 `None`，则表示没有 peek 任何元素。
    *   `stream: Fuse<T>`:  一个 `Fuse` 包装的原始流。`Fuse` 确保流在完成之后不会再次产生任何元素。

3.  **`impl<T: Stream> Peekable<T>` 块：**
    *   `new(stream: T) -> Self`:  构造函数，创建一个 `Peekable` 实例。它接收一个 `Stream` 作为参数，并使用 `fuse()` 方法将其包装成 `Fuse`，然后将 `peek` 初始化为 `None`。
    *   `peek(&mut self) -> Option<&T::Item> where T: Unpin`:  异步方法，用于查看流中的下一个元素。
        *   首先检查 `self.peek` 是否有值。如果有，则直接返回 `Some(&it)`，即返回已经 peek 过的元素的引用。
        *   如果 `self.peek` 为 `None`，则调用 `self.next().await` 从底层流中获取下一个元素，并将其存储在 `self.peek` 中。
        *   最后，返回 `self.peek.as_ref()`，即返回 peek 到的元素的引用。

4.  **`impl<T: Stream> Stream for Peekable<T>` 块：**
    *   `type Item = T::Item`:  定义了 `Peekable` 流的元素类型，与底层流的元素类型相同。
    *   `poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>>`:  实现了 `Stream` trait 的 `poll_next` 方法。
        *   首先，使用 `pin_project` 宏的 `project` 方法获取对 `Peekable` 结构体字段的投影。
        *   检查 `this.peek` 是否有值。如果有，则说明之前 peek 过一个元素，并且该元素尚未被消费。此时，将 `this.peek` 的值取出（使用 `take()` 方法），并返回 `Poll::Ready(Some(it))`。
        *   如果 `this.peek` 为 `None`，则调用 `this.stream.poll_next(cx)` 来从底层流中获取下一个元素。

**代码在项目中的作用：**
