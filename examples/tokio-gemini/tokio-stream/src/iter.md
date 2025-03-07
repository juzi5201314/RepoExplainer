这个文件定义了 `Iter` 结构体和 `iter` 函数，它们共同实现了将一个标准 Rust 迭代器转换为一个 `Stream`。`Stream` 是 `tokio-stream` crate 中的一个 trait，用于异步数据流处理。

**关键组件：**

*   **`Iter<I>` 结构体:**
    *   这是一个结构体，用于包装一个迭代器 `I`。
    *   `iter`: 存储了传入的迭代器。
    *   `yield_amt`: 用于控制 yield 的数量，防止在 `poll_next` 中过度消耗 CPU 资源。
    *   `#[derive(Debug)]`: 允许对 `Iter` 结构体进行调试打印。
    *   `#[must_use = "streams do nothing unless polled"]`: 提醒用户，`Stream` 只有被轮询时才会产生作用。
    *   `impl<I> Unpin for Iter<I> {}`: 实现了 `Unpin` trait，表示 `Iter` 可以安全地在内存中移动。

*   **`iter<I>(i: I) -> Iter<I::IntoIter>` 函数:**
    *   这是一个公共函数，用于将任何实现了 `IntoIterator` trait 的类型转换为 `Iter` 结构体。
    *   它接受一个实现了 `IntoIterator` 的类型 `i` 作为参数。
    *   它将 `i` 转换为一个迭代器 `I::IntoIter`，并用它创建一个 `Iter` 结构体。
    *   返回一个 `Iter` 结构体。

*   **`impl<I> Stream for Iter<I> where I: Iterator`:**
    *   为 `Iter` 结构体实现了 `Stream` trait。
    *   `type Item = I::Item;`: 定义了 `Stream` 的 item 类型，与底层迭代器的 item 类型相同。
    *   `fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<I::Item>>`: 这是 `Stream` trait 的核心方法，用于异步地获取下一个值。
        *   它首先检查 `yield_amt`，如果达到阈值 (32)，则重置 `yield_amt`，并调用 `cx.waker().wake_by_ref()` 唤醒任务，然后返回 `Poll::Pending`，表示当前没有新的数据可用，需要稍后再次轮询。
        *   否则，递增 `yield_amt`，并调用底层迭代器的 `next()` 方法获取下一个值。
        *   返回 `Poll::Ready(self.iter.next())`，将迭代器的下一个值包装在 `Poll::Ready` 中返回，表示有新的数据可用。
    *   `fn size_hint(&self) -> (usize, Option<usize>)`: 提供关于流大小的提示，直接调用底层迭代器的 `size_hint()` 方法。

**与项目的关系：**

这个文件是 `tokio-stream` crate 的一部分，它提供了一种将标准 Rust 迭代器适配成异步 `Stream` 的方法。这使得开发者可以使用熟悉的迭代器模式来处理异步数据流，简化了异步编程。`iter` 函数是 `tokio-stream` crate 中一个基础且常用的功能，它允许将同步数据源（如 `Vec`、`Range` 等）转换为异步数据流，方便与其他异步操作进行组合和处理。
