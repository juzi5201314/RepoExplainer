这个文件定义了一系列用于从异步读取器中读取整数的 Future。它使用 `pin_project_lite` crate 来创建自引用结构体，并使用 `bytes` crate 来处理字节缓冲区。

**主要组成部分：**

1.  **宏 `reader!` 和 `reader8!`**:
    *   这两个宏用于生成读取不同整数类型（例如 `u8`, `u16`, `u32` 等）的 Future。
    *   `reader!` 宏处理多字节整数，它创建一个包含源读取器 (`src`)、缓冲区 (`buf`) 和读取计数 (`read`) 的结构体。它循环调用 `poll_read` 从源读取数据，直到缓冲区填满，然后使用 `bytes::Buf` trait 的相关方法（例如 `get_u16`）从缓冲区中读取整数。
    *   `reader8!` 宏处理单字节整数 (u8, i8)，它创建一个包含源读取器 (`reader`) 的结构体，并直接从读取器中读取一个字节。
    *   `PhantomPinned` 用于确保生成的 Future 不可移动，这对于与异步 trait 方法的兼容性至关重要。

2.  **结构体**:
    *   宏生成的结构体，例如 `ReadU8`, `ReadU16`, `ReadI32Le` 等，它们实现了 `Future` trait。
    *   每个结构体都包含一个异步读取器 (`src` 或 `reader`)，以及一个用于存储读取数据的缓冲区 (`buf`)。

3.  **`Future` 实现**:
    *   每个结构体都实现了 `Future` trait，定义了 `poll` 方法。
    *   `poll` 方法负责从异步读取器中读取数据，并将其转换为指定的整数类型。
    *   如果读取操作未完成，`poll` 方法将返回 `Poll::Pending`。
    *   如果读取操作成功，`poll` 方法将返回 `Poll::Ready(Ok(整数值))`。
    *   如果发生错误（例如，遇到 `UnexpectedEof`），`poll` 方法将返回 `Poll::Ready(Err(错误))`。

**工作流程：**

1.  创建一个具体的读取整数的 Future 实例 (例如 `ReadU32::new(reader)`)。
2.  在异步代码中使用 `.await` 或手动调用 `poll` 方法来驱动 Future。
3.  `poll` 方法会尝试从底层的 `AsyncRead` 中读取数据。
4.  如果数据足够，`poll` 方法将数据转换为指定的整数类型，并返回 `Poll::Ready(Ok(整数值))`。
5.  如果数据不足，`poll` 方法将返回 `Poll::Pending`，等待更多数据到达。
6.  如果发生错误，`poll` 方法将返回 `Poll::Ready(Err(错误))`。

**与项目的关系：**

这个文件提供了从异步读取器中读取各种整数类型的 Future，是 Tokio I/O 库的一部分，用于实现异步读取整数的功能。这些 Future 可以被用于构建更高级的异步 I/O 操作，例如解析网络协议或从文件中读取二进制数据。
