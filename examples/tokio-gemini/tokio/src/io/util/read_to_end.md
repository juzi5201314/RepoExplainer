这个文件定义了 `ReadToEnd` 结构体和相关的函数，用于异步读取数据直到读取结束。它的主要目的是实现 `AsyncRead` trait 的 `read_to_end` 方法，将数据从异步读取器读取到 `Vec<u8>` 缓冲区中。

**关键组件：**

*   **`ReadToEnd<'a, R: ?Sized>` 结构体:**
    *   这是一个 `Future`，用于异步读取数据。
    *   `reader: &'a mut R`:  对实现 `AsyncRead` trait 的读取器的可变引用。
    *   `buf: VecWithInitialized<&'a mut Vec<u8>>`:  一个包装了 `Vec<u8>` 的结构体，用于存储读取到的数据。`VecWithInitialized` 确保了缓冲区的初始化。
    *   `read: usize`:  记录已经读取到 `buf` 中的字节数。
    *   `_pin: PhantomPinned`:  用于实现 `!Unpin`，以兼容异步 trait 方法。

*   **`read_to_end<'a, R>(reader: &'a mut R, buffer: &'a mut Vec<u8>) -> ReadToEnd<'a, R>` 函数:**
    *   创建一个 `ReadToEnd` 实例，初始化读取器和缓冲区。

*   **`read_to_end_internal<V: VecU8, R: AsyncRead + ?Sized>(...) -> Poll<io::Result<usize>>` 函数:**
    *   核心的读取逻辑。
    *   它在一个循环中调用 `poll_read_to_end` 函数，直到读取器返回错误或读取到 0 字节（表示读取结束）。
    *   `num_read` 参数用于累加读取的字节数。

*   **`poll_read_to_end<V: VecU8, R: AsyncRead + ?Sized>(...) -> Poll<io::Result<usize>>` 函数:**
    *   尝试从读取器读取数据，并将其追加到缓冲区 `buf` 中。
    *   它使用一个自适应的策略来扩展缓冲区，以避免不必要的内存分配。
    *   首先尝试使用一个小的缓冲区读取，如果读取到数据，则将数据追加到主缓冲区。如果小缓冲区读取没有读取到数据，则根据需要扩展主缓冲区。
    *   使用 `ReadBuf` 来安全地读取数据到缓冲区。

*   **`impl<A> Future for ReadToEnd<'_, A>`:**
    *   为 `ReadToEnd` 结构体实现 `Future` trait。
    *   `poll` 方法调用 `read_to_end_internal` 来执行实际的读取操作。

**工作流程：**

1.  `read_to_end` 函数创建一个 `ReadToEnd` 实例。
2.  当 `ReadToEnd` 的 `Future` 被 `poll` 时，它会调用 `read_to_end_internal`。
3.  `read_to_end_internal` 在一个循环中调用 `poll_read_to_end`。
4.  `poll_read_to_end` 尝试从读取器读取数据，并将其追加到缓冲区。
5.  如果读取器返回错误或读取到 0 字节，`read_to_end_internal` 结束，`Future` 完成。
