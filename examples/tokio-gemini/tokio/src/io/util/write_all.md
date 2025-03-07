这个文件定义了一个名为 `WriteAll` 的结构体，它实现了 `Future` trait，用于异步地将一个字节切片完整地写入一个实现了 `AsyncWrite` trait 的 writer。

**主要组成部分：**

1.  **`WriteAll` 结构体:**
    *   使用 `pin_project!` 宏进行投影，确保结构体字段在 `Pin` 状态下可以安全地访问。
    *   `writer`:  一个对实现了 `AsyncWrite` trait 的 writer 的可变引用。
    *   `buf`:  一个指向要写入的字节切片的引用。
    *   `_pin`:  一个 `PhantomPinned` 字段，用于确保 `WriteAll` 结构体在内存中是不可移动的，这对于与异步 trait 方法的兼容性至关重要。

2.  **`write_all` 函数:**
    *   这是一个辅助函数，用于创建一个 `WriteAll` 实例。
    *   它接受一个实现了 `AsyncWrite` trait 的 writer 的可变引用和一个字节切片作为参数。
    *   它返回一个 `WriteAll` 结构体的实例，该实例封装了 writer 和要写入的缓冲区。

3.  **`Future` trait 的实现:**
    *   `type Output = io::Result<()>`:  定义了 `Future` 的输出类型，表示写入操作的结果，成功则返回 `Ok(())`，失败则返回 `io::Error`。
    *   `poll` 方法:
        *   这是 `Future` trait 的核心方法，用于轮询写入操作的完成情况。
        *   它首先通过 `self.project()` 创建一个投影，以便安全地访问结构体的字段。
        *   它在一个 `while` 循环中，只要缓冲区 `buf` 还有未写入的数据，就重复执行以下操作：
            *   调用 `writer.poll_write()` 尝试将数据写入 writer。
            *   如果写入成功，则更新 `buf`，使其指向剩余未写入的数据。
            *   如果 `poll_write` 返回 `Poll::Ready(Ok(0))`，表示 writer 无法写入更多数据，则返回 `io::ErrorKind::WriteZero` 错误。
        *   当 `buf` 为空时，表示所有数据都已成功写入，返回 `Poll::Ready(Ok(()))`。

**与项目的关系：**

这个文件提供了一个异步写入所有数据的工具，是 Tokio 异步 I/O 库的一部分。它允许用户安全且高效地将数据写入实现了 `AsyncWrite` trait 的 writer，确保所有数据都被写入，或者在写入失败时返回错误。它封装了底层的异步 I/O 操作，并提供了一个易于使用的 `Future` 接口，方便用户在异步程序中使用。
