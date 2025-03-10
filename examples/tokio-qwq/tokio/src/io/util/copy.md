### 代码文件解释：`tokio/src/io/util/copy.rs`

#### 目的
该文件实现了 Tokio 异步 I/O 框架中的 `copy` 函数，用于在异步读取器（`AsyncRead`）和异步写入器（`AsyncWrite`）之间高效传输数据。通过缓冲机制和非阻塞操作，确保异步环境下的数据复制高效且线程安全。

---

#### 核心组件

1. **`CopyBuffer` 结构体**
   - **功能**：管理缓冲区状态，协调读取和写入操作。
   - **关键字段**：
     - `buf`: 内存缓冲区（大小由 `buf_size` 指定）。
     - `read_done`: 标记是否已读取完所有数据。
     - `need_flush`: 标记是否需要刷新写入器。
     - `pos/cap`: 分别表示缓冲区当前读写位置和已填充数据长度。
     - `amt`: 已传输的总字节数。
   - **方法**：
     - `new()`: 初始化缓冲区。
     - `poll_fill_buf()`: 非阻塞填充缓冲区，从读取器读取数据。
     - `poll_write_buf()`: 将缓冲区数据写入写入器，处理写入阻塞情况。
     - `poll_copy()`: 主循环逻辑，交替填充缓冲区和写入数据，直到传输完成。

2. **`Copy` Future**
   - **功能**：封装 `CopyBuffer` 和读写器，作为可等待的 Future。
   - **实现**：
     - 通过 `poll` 方法调用 `CopyBuffer.poll_copy()` 驱动异步操作。
     - 返回传输的总字节数或错误。

3. **`copy` 函数**
   - **功能**：公开的入口函数，返回 `Copy` Future。
   - **参数**：需要实现 `AsyncRead` 和 `AsyncWrite` 的读写器。
   - **默认配置**：使用 `DEFAULT_BUF_SIZE`（通常为 8KB）作为缓冲区大小。

---

#### 工作原理
1. **缓冲机制**：
   - 使用固定大小的缓冲区（`CopyBuffer.buf`）暂存数据，平衡读写速度差异。
   - 当缓冲区未满且读取未完成时，持续填充缓冲区（`poll_fill_buf`）。
   - 当缓冲区有数据时，尝试写入（`poll_write_buf`），若写入阻塞则尝试填充更多数据。

2. **非阻塞循环**：
   - `poll_copy` 方法通过无限循环交替执行读取和写入：
     1. 尝试填充缓冲区，若读取阻塞则检查缓冲区是否为空，否则继续。
     2. 将缓冲区数据写入目标，若写入阻塞则暂停，等待下次轮询。
     3. 写入完成后重置缓冲区，重复直至读取完成。
   - 最终刷新写入器并返回总传输字节数。

3. **错误处理**：
   - 任何读取或写入错误会立即终止传输并返回错误。
   - 写入零字节视为错误（`WriteZero`）。

---

#### 项目中的角色
该文件是 Tokio 异步 I/O 工具的核心组件之一，提供高效的异步数据复制功能，支持在异步流（如网络套接字、文件）之间无缝传输数据，是构建更高层 I/O 操作（如文件传输、协议解析）的基础。
