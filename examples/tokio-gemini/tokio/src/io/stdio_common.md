这个文件定义了一个名为 `SplitByUtf8BoundaryIfWindows` 的结构体，它是一个 `AsyncWrite` 的适配器，主要用于处理标准输出（stdout）和标准错误输出（stderr）。它的主要目的是在 Windows 平台上，确保写入到标准输出的内容是有效的 UTF-8 编码。

**关键组件：**

*   **`SplitByUtf8BoundaryIfWindows<W>` 结构体:**
    *   `inner: W`:  一个泛型参数 `W`，它实现了 `AsyncWrite` trait。这个 `inner` 字段持有实际的写入器，例如 `Stdout` 或 `Stderr`。
    *   `new(inner: W)`: 构造函数，用于创建一个 `SplitByUtf8BoundaryIfWindows` 实例，并将给定的写入器 `inner` 包装起来。
*   **`poll_write` 方法 (核心逻辑):**
    *   这个方法是 `AsyncWrite` trait 的实现，负责将数据写入底层的写入器。
    *   **平台检查:**  首先检查当前操作系统是否为 Windows 或是否为测试环境。只有在 Windows 上，才需要进行 UTF-8 编码的检查和处理。
    *   **缓冲区大小限制:**  如果缓冲区大小超过 `DEFAULT_MAX_BUF_SIZE`，则将其截断。
    *   **UTF-8 编码检查:**  检查缓冲区的前 `MAX_BYTES_PER_CHAR * MAGIC_CONST` 字节是否为有效的 UTF-8 编码。
        *   如果确定是 UTF-8 编码，则从缓冲区末尾移除不完整的 UTF-8 字符，以确保写入的数据是完整的 UTF-8 字符。
        *   如果不是 UTF-8 编码，则不进行截断，直接将缓冲区写入。
    *   **调用内部写入器:**  最后，调用内部写入器 `inner` 的 `poll_write` 方法，将处理后的数据写入。
*   **`poll_flush` 和 `poll_shutdown` 方法:**
    *   这两个方法分别用于刷新和关闭写入器，它们简单地将调用转发给内部写入器 `inner`。
*   **常量:**
    *   `MAX_BYTES_PER_CHAR`:  UTF-8 编码中一个字符最多占用的字节数（4）。
    *   `MAGIC_CONST`:  用于 UTF-8 编码检查的常量。
*   **测试模块 (`#[cfg(test)]`)**:
    *   包含一些测试用例，用于验证 `SplitByUtf8BoundaryIfWindows` 的功能，包括：
        *   `test_splitter`:  测试写入大量数据时，是否正确截断缓冲区。
        *   `test_pseudo_text`:  测试写入部分二进制数据时，是否正确处理。

**如何融入项目：**

这个文件定义了一个用于处理标准输出和标准错误输出的适配器，它主要用于 Windows 平台，以确保写入的数据是有效的 UTF-8 编码。它被用于 `Stdout` 和 `Stderr` 的实现中，例如，在 `tokio::io` 模块中，`Stdout` 结构体使用 `SplitByUtf8BoundaryIfWindows` 来包装底层的 `std::io::Stdout`。
