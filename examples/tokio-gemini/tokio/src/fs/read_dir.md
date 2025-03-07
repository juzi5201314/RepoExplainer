这个文件定义了 `tokio` 异步文件系统模块中用于读取目录内容的结构和函数。它的主要目的是提供一个异步的、基于 `tokio` 的 `read_dir` 功能，类似于标准库中的 `std::fs::read_dir`，但它不会阻塞当前线程。

**主要组件：**

*   **`read_dir(path: impl AsRef<Path>) -> io::Result<ReadDir>`**:  这是一个异步函数，用于打开一个目录并返回一个 `ReadDir` 结构体。它首先将给定的路径转换为 `PathBuf`，然后使用 `asyncify` 函数在后台线程中执行 `std::fs::read_dir`，以避免阻塞。`asyncify` 是 `tokio` 提供的用于在异步上下文中使用阻塞操作的工具。它初始化一个 `ReadDir` 结构体，该结构体包含一个内部状态 `State`。
*   **`ReadDir(State)`**:  这是一个结构体，表示一个目录的读取器。它实现了 `Stream` 特征，允许异步迭代目录中的条目。它包含一个 `State` 字段，用于跟踪读取器的状态。
*   **`State`**:  一个枚举，表示 `ReadDir` 的内部状态。它可以是 `Idle`（表示读取器空闲，准备读取下一个块）或 `Pending`（表示正在后台线程中执行读取操作）。
*   **`next_entry(&mut self) -> io::Result<Option<DirEntry>>`**:  这是一个异步方法，用于从目录读取下一个条目。它使用 `poll_next_entry` 来轮询底层的读取操作。
*   **`poll_next_entry(&mut self, cx: &mut Context<'_>) -> Poll<io::Result<Option<DirEntry>>>`**:  这是一个轮询方法，用于检查是否有下一个目录条目可用。它处理 `State` 的转换，在 `Idle` 和 `Pending` 状态之间切换，并在后台线程中执行读取操作。它使用 `spawn_blocking` 在一个单独的线程中执行阻塞的 `std::fs::read_dir` 操作。
*   **`next_chunk(buf: &mut VecDeque<io::Result<DirEntry>>, std: &mut std::fs::ReadDir) -> bool`**:  这个函数从 `std::fs::ReadDir` 中读取一批目录条目（CHUNK\_SIZE 个），并将它们存储在 `VecDeque` 中。它处理读取错误，并将结果封装在 `DirEntry` 中。
*   **`DirEntry`**:  这是一个结构体，表示目录中的一个条目。它封装了 `std::fs::DirEntry`，并提供了访问文件路径、文件名、元数据和文件类型的方法。它还实现了特定于 Unix 系统的 `ino()` 方法，用于获取 inode 编号。
*   **`asyncify`**:  一个辅助函数，用于在后台线程中运行阻塞的 I/O 操作，并将其结果转换为异步结果。

**工作流程：**

1.  调用 `read_dir` 函数创建一个 `ReadDir` 实例。
2.  调用 `next_entry` 或 `poll_next_entry` 来获取目录中的条目。
3.  `poll_next_entry` 检查内部状态。
    *   如果状态是 `Idle`，它会从内部缓冲区中返回一个条目，或者如果缓冲区为空，则启动一个后台任务来读取下一个块。
    *   如果状态是 `Pending`，它会轮询后台任务的结果。
4.  后台任务使用 `spawn_blocking` 在一个单独的线程中执行 `std::fs::read_dir`。
5.  `next_chunk` 函数从 `std::fs::ReadDir` 中读取条目，并将它们存储在内部缓冲区中。
6.  `DirEntry` 结构体提供了访问文件信息的接口。

**与其他组件的交互：**

*   **`asyncify`**:  用于在后台线程中执行阻塞的 `std::fs::read_dir` 操作。
*   **`spawn_blocking`**:  用于在后台线程中生成任务，以执行阻塞的 I/O 操作。
*   **`DirEntry`**:  与 `ReadDir` 交互，提供对目录条目的访问。
