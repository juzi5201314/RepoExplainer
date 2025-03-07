这个文件实现了在两个异步读写流之间进行双向数据拷贝的功能。它定义了几个核心函数，用于高效地在两个流之间传输数据。

**核心组件：**

1.  **`TransferState` 枚举：**
    *   `Running(CopyBuffer)`: 表示正在进行数据拷贝，并持有用于拷贝数据的 `CopyBuffer`。
    *   `ShuttingDown(u64)`: 表示已经检测到一端流的结束（EOF），正在关闭另一端流，`u64` 存储了已经拷贝的字节数。
    *   `Done(u64)`: 表示已经完成一个方向的数据拷贝，`u64` 存储了已经拷贝的字节数。

2.  **`transfer_one_direction<A, B>` 函数：**
    *   这个函数是核心的拷贝逻辑。它负责在一个方向上（例如，从 `a` 到 `b`）进行数据拷贝。
    *   它使用 `CopyBuffer` 来缓存数据，并使用 `poll_copy` 方法进行异步拷贝。
    *   当检测到源流结束时，它会调用目标流的 `poll_shutdown` 方法来关闭连接。
    *   它使用 `TransferState` 来跟踪拷贝的进度。

3.  **`copy_bidirectional<A, B>` 函数：**
    *   这是一个公共的 API 函数，用于启动双向数据拷贝。
    *   它使用默认的缓冲区大小（`super::DEFAULT_BUF_SIZE`）。
    *   它调用 `copy_bidirectional_impl` 函数来执行实际的拷贝操作。

4.  **`copy_bidirectional_with_sizes<A, B>` 函数：**
    *   这个函数类似于 `copy_bidirectional`，但允许用户指定用于拷贝的缓冲区大小。
    *   它也调用 `copy_bidirectional_impl` 函数。

5.  **`copy_bidirectional_impl<A, B>` 函数：**
    *   这是实际执行双向拷贝的函数。
    *   它创建了两个 `TransferState` 实例，分别用于 `a` 到 `b` 和 `b` 到 `a` 的数据拷贝。
    *   它使用 `poll_fn` 和 `transfer_one_direction` 函数来并发地执行两个方向的数据拷贝。
    *   当两个方向都完成时，它返回拷贝的字节数。

**工作流程：**

1.  `copy_bidirectional` 或 `copy_bidirectional_with_sizes` 函数被调用，启动双向拷贝。
2.  `copy_bidirectional_impl` 函数被调用，创建两个 `TransferState` 实例，并使用 `poll_fn` 启动一个异步任务。
3.  异步任务并发地调用 `transfer_one_direction` 函数，分别处理 `a` 到 `b` 和 `b` 到 `a` 的数据拷贝。
4.  `transfer_one_direction` 函数使用 `CopyBuffer` 缓存数据，并使用 `poll_copy` 进行异步拷贝。
5.  当检测到一端流的结束时，`transfer_one_direction` 函数会关闭另一端流。
6.  当两个方向都完成拷贝时，异步任务返回拷贝的字节数。

**与其他组件的关系：**

*   它使用了 `super::copy::CopyBuffer` 来进行数据拷贝。
*   它使用了 `crate::io::{AsyncRead, AsyncWrite}` trait 来抽象异步读写流。
*   它使用了 `std::future::poll_fn` 和 `std::task::{ready, Context, Poll}` 来实现异步操作。
