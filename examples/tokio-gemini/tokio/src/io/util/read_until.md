这个文件定义了 `ReadUntil` 结构体和相关的函数，用于异步读取数据直到遇到特定的分隔符。它实现了 `AsyncBufReadExt` trait 的 `read_until` 方法。

**主要组成部分：**

1.  **`ReadUntil` 结构体:**
    *   这是一个 `Future`，用于异步读取数据。
    *   它包含一个对 `AsyncBufRead` trait 的实现者的引用 (`reader`)，一个分隔符 (`delimiter`)，一个用于存储读取数据的缓冲区 (`buf`)，以及一个记录已读取字节数的 `read` 字段。
    *   `_pin: PhantomPinned` 用于确保 `ReadUntil` 不可移动，这对于与异步 trait 方法的兼容性至关重要。

2.  **`read_until` 函数:**
    *   这是一个创建 `ReadUntil` 实例的工厂函数。
    *   它接收一个 `AsyncBufRead` 的可变引用，一个分隔符和一个缓冲区，并返回一个 `ReadUntil` 实例。

3.  **`read_until_internal` 函数:**
    *   这是 `ReadUntil` 的核心逻辑。
    *   它接收一个 `Pin<&mut R>` (指向 `AsyncBufRead` trait 实现者的指针)，一个上下文 `Context`，分隔符，缓冲区和已读取字节数的引用。
    *   它在一个循环中工作，不断从 reader 中读取数据，直到找到分隔符或读取操作完成。
    *   它使用 `poll_fill_buf` 从 reader 中获取数据，使用 `memchr` 查找分隔符，并将数据追加到缓冲区。
    *   它使用 `consume` 告知 reader 已经处理了多少数据。
    *   它返回 `Poll::Ready(Ok(usize))` 表示成功读取，或者 `Poll::Pending` 表示需要等待。

4.  **`Future` 的实现:**
    *   `impl<R: AsyncBufRead + ?Sized + Unpin> Future for ReadUntil<'_, R>` 为 `ReadUntil` 结构体实现了 `Future` trait。
    *   `poll` 方法是 `Future` trait 的核心。它调用 `read_until_internal` 函数来执行实际的读取操作。

**工作流程：**

1.  调用 `read_until` 函数创建一个 `ReadUntil` 实例。
2.  在 `Future` 的 `poll` 方法中，`read_until_internal` 函数被反复调用，直到读取到分隔符或发生错误。
3.  `read_until_internal` 函数从 `AsyncBufRead` 中读取数据，查找分隔符，并将数据追加到缓冲区。
4.  当找到分隔符时，`read_until_internal` 函数返回 `Poll::Ready(Ok(usize))`，表示读取完成。

**与其他组件的关系：**

*   它实现了 `AsyncBufReadExt` trait 的 `read_until` 方法，允许异步读取数据直到遇到指定的分隔符。
*   它使用了 `memchr` crate 来高效地查找分隔符。
*   它依赖于 `AsyncBufRead` trait，该 trait 提供了异步读取缓冲数据的能力。
