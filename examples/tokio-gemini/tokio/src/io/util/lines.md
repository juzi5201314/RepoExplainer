这个文件定义了 `Lines` 结构体，它用于从实现了 `AsyncBufRead` trait 的异步读取器中逐行读取文本。它提供了异步读取文本行的功能，并与 `tokio-stream` crate 结合使用，可以将 `Lines` 转换为 `Stream`。

**主要组件：**

*   **`Lines<R>` 结构体:**
    *   `reader`: 封装了底层的异步读取器，实现了 `AsyncBufRead` trait。
    *   `buf`: 用于存储当前读取的行的字符串缓冲区。
    *   `bytes`: 用于存储中间读取的字节的 `Vec<u8>`。
    *   `read`: 记录已读取的字节数。
*   **`lines<R>(reader: R) -> Lines<R>` 函数:**
    *   创建一个 `Lines` 实例，初始化内部缓冲区。
*   **`next_line(&mut self) -> io::Result<Option<String>>` 方法:**
    *   异步地从读取器中读取下一行文本。
    *   使用 `poll_fn` 将 `poll_next_line` 转换为一个 `Future`。
*   **`get_mut(&mut self) -> &mut R` 和 `get_ref(&mut self) -> &R` 方法:**
    *   分别提供对底层读取器的可变和不可变引用。
*   **`into_inner(self) -> R` 方法:**
    *   返回底层的读取器，并放弃内部缓冲区中的任何剩余数据。
*   **`poll_next_line(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<Option<String>>>` 方法:**
    *   核心方法，用于轮询读取下一行。
    *   使用 `read_line_internal` 从读取器中读取数据。
    *   处理行尾的换行符 (`\n` 和 `\r\n`)。
    *   返回 `Poll::Ready(Ok(Some(line)))` 表示成功读取一行，`Poll::Ready(Ok(None))` 表示读取结束，`Poll::Pending` 表示数据尚未准备好，或者 `Poll::Ready(Err(err))` 表示发生 I/O 错误。
*   **`tests` 模块:**
    *   包含一个测试用例 `assert_unpin`，用于断言 `Lines` 结构体实现了 `Unpin` trait。

**与其他部分的关系：**

*   `Lines` 结构体实现了 `AsyncBufReadExt::lines` 方法，该方法用于创建 `Lines` 实例。
*   `Lines` 结构体与 `tokio-stream` crate 结合使用，可以通过 `LinesStream` 将其转换为一个 `Stream`，从而可以方便地使用 `Stream` 的各种方法来处理文本行。
*   `read_line_internal` 函数是 `Lines` 内部使用的辅助函数，用于从 `AsyncBufRead` 中读取一行。
