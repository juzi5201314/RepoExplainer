这个文件定义了用于在内存中进行 I/O 操作的结构体和函数。它提供了两种主要的结构体：`DuplexStream` 和 `SimplexStream`，以及用于创建它们的函数 `duplex` 和 `simplex`。

*   **`DuplexStream`**:
    *   表示一个双向管道，用于在内存中读写字节。
    *   它由两个 `SimplexStream` 组成，一个用于读取，一个用于写入。
    *   `duplex` 函数创建一对 `DuplexStream`，它们就像连接的套接字一样，写入一个端点的数据可以从另一个端点读取。
    *   当一个 `DuplexStream` 的一端被丢弃时，另一端的未完成读取将继续读取数据直到缓冲区耗尽，然后通过返回 0 字节来发出 EOF 信号。对另一端的写入将立即返回 `Err(BrokenPipe)`。
    *   实现了 `AsyncRead` 和 `AsyncWrite` trait，允许异步读写操作。
    *   使用 `Arc<Mutex<SimplexStream>>` 来实现多线程安全。

*   **`SimplexStream`**:
    *   表示一个单向管道，用于在内存中读写字节。
    *   可以由 `simplex` 函数创建，该函数创建一对 reader 和 writer，或者通过调用 `SimplexStream::new_unsplit` 创建一个同时用于读写操作的句柄。
    *   包含一个 `BytesMut` 类型的缓冲区，用于存储写入的数据。
    *   `is_closed` 标志指示写入端是否已关闭。
    *   `max_buf_size` 限制了在返回 `Poll::Pending` 之前可以写入的最大字节数。
    *   `read_waker` 和 `write_waker` 用于存储等待读写操作完成的任务的唤醒器。
    *   实现了 `AsyncRead` 和 `AsyncWrite` trait，允许异步读写操作。
    *   `close_write` 和 `close_read` 方法用于关闭管道的读写端，并唤醒等待的任务。
    *   `poll_read_internal` 和 `poll_write_internal` 方法实现了底层的读写逻辑。

*   **`duplex(max_buf_size: usize) -> (DuplexStream, DuplexStream)`**:
    *   创建一个新的 `DuplexStream` 对，模拟连接的套接字。
    *   `max_buf_size` 参数指定在写入操作返回 `Poll::Pending` 之前可以写入的最大字节数。

*   **`simplex(max_buf_size: usize) -> (ReadHalf<SimplexStream>, WriteHalf<SimplexStream>)`**:
    *   创建一个单向的 `SimplexStream`，返回一个读端和一个写端。
    *   `max_buf_size` 参数指定在写入操作返回 `Poll::Pending` 之前可以写入的最大字节数。

*   **`SimplexStream::new_unsplit(max_buf_size: usize) -> SimplexStream`**:
    *   创建一个同时支持读写操作的 `SimplexStream`。
    *   `max_buf_size` 参数指定在写入操作返回 `Poll::Pending` 之前可以写入的最大字节数。

该文件提供了一种在内存中进行异步 I/O 操作的机制，这对于测试、模拟网络连接或在内存中传递数据非常有用。
