这段代码文件实现了 `tokio` 库中用于异步读取一行文本的功能。它定义了一个名为 `ReadLine` 的 `Future`，用于异步地从实现了 `AsyncBufRead` trait 的读取器中读取一行文本，直到遇到换行符 `\n`。

**关键组件：**

1.  **`ReadLine` 结构体:**
    *   这是一个 `Future`，用于异步读取一行文本。
    *   `reader`:  对实现了 `AsyncBufRead` trait 的读取器的可变引用。
    *   `output`:  对用于存储读取到的文本的 `String` 的可变引用。在读取过程中，`output` 会被暂时替换为空字符串，以避免在读取过程中进行 UTF-8 编码处理。
    *   `buf`:  一个 `Vec<u8>`，用于存储从读取器读取的原始字节数据。
    *   `read`:  记录已经添加到 `buf` 中的字节数。
    *   `_pin`:  一个 `PhantomPinned` 字段，用于确保 `ReadLine` 结构体不可移动，这对于与异步 trait 方法的兼容性至关重要。

2.  **`read_line` 函数:**
    *   这是一个辅助函数，用于创建 `ReadLine` 结构体的实例。
    *   它接收一个实现了 `AsyncBufRead` trait 的读取器和一个 `String` 作为输入。
    *   它将 `String` 的内容移动到 `buf` 中，并将 `String` 设置为空字符串。
    *   它初始化 `ReadLine` 结构体的其他字段，并返回该结构体的实例。

3.  **`put_back_original_data` 函数:**
    *   当发生 UTF-8 解码错误时，该函数用于将原始数据放回 `output` 字符串。

4.  **`finish_string_read` 函数:**
    *   处理读取操作的各种失败情况，并将结果放回 `output`。
    *   它处理 `IO` 错误和 UTF-8 解码错误。
    *   根据错误类型，它将数据放回 `output`，并返回相应的 `Poll` 结果。

5.  **`read_line_internal` 函数:**
    *   这是 `ReadLine` 的核心逻辑。
    *   它使用 `read_until_internal` 函数（未在此文件中定义，但可以推断其功能）从读取器中读取数据，直到遇到换行符 `\n`。
    *   它将读取到的字节数据转换为 `String`。
    *   它调用 `finish_string_read` 函数来处理可能的错误。

6.  **`Future` 的 `poll` 实现:**
    *   `ReadLine` 结构体实现了 `Future` trait。
    *   `poll` 方法调用 `read_line_internal` 函数来执行实际的读取操作。

**工作流程：**

1.  `read_line` 函数创建一个 `ReadLine` 结构体的实例。
2.  当 `ReadLine` 的 `poll` 方法被调用时，它会调用 `read_line_internal` 函数。
3.  `read_line_internal` 函数使用 `read_until_internal` 函数从读取器中读取数据，直到遇到换行符。
4.  读取到的字节数据被转换为 `String`。
5.  `finish_string_read` 函数处理可能的 `IO` 错误和 UTF-8 解码错误，并将结果返回。
6.  `poll` 方法返回 `Poll::Ready` 或 `Poll::Pending`，指示操作是否完成。

**与其他组件的交互：**

*   它使用了 `read_until_internal` 函数，该函数负责实际的读取操作。
*   它实现了 `Future` trait，使得它可以被 `tokio` 的任务调度器执行。
*   它使用了 `AsyncBufRead` trait，这定义了异步缓冲读取器的接口。
