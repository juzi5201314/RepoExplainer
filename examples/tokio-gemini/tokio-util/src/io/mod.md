这个文件 `src/io/mod.rs` 包含了用于处理 I/O 相关任务的辅助工具。它主要用于 Tokio 异步 I/O 操作，并提供了一些方便的类型和函数，例如将 `hyper::Body` 转换为 `AsyncRead`。

**关键组件：**

*   **模块声明：**  文件定义了多个子模块，包括 `copy_to_bytes`、`inspect`、`read_buf`、`reader_stream`、`sink_writer` 和 `stream_reader`。这些模块分别实现了不同的 I/O 辅助功能。
*   **条件编译：** 使用 `cfg_io_util!` 宏来条件编译 `read_arc` 和 `sync_bridge` 模块。这允许根据不同的编译配置启用或禁用某些功能。
*   **公共导出：**  通过 `pub use` 语句，将子模块中的一些类型和函数导出到当前模块的命名空间，使得它们可以被其他模块使用。例如，`CopyToBytes`、`InspectReader`、`InspectWriter`、`read_buf`、`ReaderStream`、`SinkWriter`、`StreamReader` 和 `read_exact_arc`。
*   **`SyncIoBridge`：**  这个类型用于将异步 I/O 转换为同步 I/O，这在 `tokio::task::spawn_blocking` 中使用同步 API 时非常有用。
*   **`poll_read_buf` 和 `poll_write_buf`：**  从 `crate::util` 模块导入，用于轮询读取和写入缓冲区。

**与其他组件的关联：**

*   **`hyper` 和 `reqwest`：**  这些库经常与流类型结合使用，允许在 `hyper::Body` 和 `AsyncRead` 之间进行转换。
*   **`tokio::io`：**  该模块是 Tokio 异步 I/O 的核心，提供了 `AsyncRead`、`AsyncWrite` 和 `AsyncBufRead` 等 trait。
*   **`tokio::task::spawn_blocking`：**  `SyncIoBridge` 类型通常用于在 `spawn_blocking` 中使用同步 API。

**总结：**

该文件定义了 Tokio 中用于 I/O 操作的辅助工具，包括各种 Reader 和 Writer 的封装，以及用于异步和同步 I/O 转换的桥接器。
