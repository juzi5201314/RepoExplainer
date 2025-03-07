这个文件定义了一个模拟的 `AsyncRead` 和 `AsyncWrite` 类型，用于在 Tokio 异步 I/O 操作的测试中。它允许开发者模拟网络连接的行为，通过预先定义读写操作的序列来控制模拟 I/O 的行为。

**主要组成部分：**

*   **`Mock` 结构体：** 实现了 `AsyncRead` 和 `AsyncWrite` trait，是模拟 I/O 的核心。它根据预定义的 `Action` 序列来响应读写操作。
*   **`Handle` 结构体：** 允许在 `Mock` 实例创建后，通过发送 `Action` 来动态地向模拟 I/O 添加操作。
*   **`Builder` 结构体：** 用于构建 `Mock` 实例。它允许开发者定义一系列的读、写、等待操作，从而构建一个模拟的 I/O 场景。
*   **`Action` 枚举：** 定义了模拟 I/O 可以执行的动作，包括 `Read`（读取数据）、`Write`（写入数据）、`Wait`（等待一段时间）、`ReadError`（读取错误）和 `WriteError`（写入错误）。
*   **`Inner` 结构体：** 包含 `Mock` 的内部状态，如待执行的 `Action` 队列、等待时间、睡眠状态、唤醒器和接收 `Action` 的通道。

**工作原理：**

1.  **构建模拟：** 使用 `Builder` 定义一系列 `Action`，然后调用 `build` 方法创建 `Mock` 实例。
2.  **I/O 操作：** 当测试代码调用 `AsyncRead` 或 `AsyncWrite` 的方法时，`Mock` 会从其内部的 `actions` 队列中取出相应的 `Action`。
3.  **处理 Action：**
    *   `Read`：返回预先定义的数据。
    *   `Write`：验证写入的数据是否与预定义的数据匹配。
    *   `Wait`：模拟等待一段时间。
    *   `ReadError` / `WriteError`：返回预定义的错误。
4.  **错误处理：** 如果模拟 I/O 遇到未预期的操作，例如写入了未定义的数据，则会触发 panic。
5.  **动态添加操作：** 使用 `Handle` 可以在 `Mock` 实例创建后，通过发送 `Action` 来动态地向模拟 I/O 添加操作。

**与其他部分的关联：**

*   `tokio::io`：实现了 `AsyncRead` 和 `AsyncWrite` trait，模拟了异步 I/O 的行为。
*   `tokio::sync::mpsc`：用于 `Handle` 和 `Inner` 之间的通信，允许在运行时向模拟 I/O 添加操作。
*   `tokio::time`：用于模拟等待操作。
*   `tokio_stream`：用于接收来自 `Handle` 的 `Action`。
*   `futures_core`：用于实现 `Stream` trait。
*   `std::collections::VecDeque`：用于存储 `Action` 队列。
*   `std::sync::Arc`：用于在 `Action` 中共享错误。
