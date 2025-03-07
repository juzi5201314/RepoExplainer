这个文件定义了 `Blocking` 结构体，它为同步 `Read` 和 `Write` 操作提供了一个异步包装器。它允许在异步上下文中执行阻塞的 I/O 操作。

**主要组成部分：**

*   **`Blocking<T>` 结构体:**
    *   `inner`: 包含底层同步 I/O 对象的 `Option`。
    *   `state`: 一个 `State` 枚举，表示当前 I/O 操作的状态（空闲或繁忙）。
    *   `need_flush`: 一个布尔值，指示底层 I/O 层是否需要刷新。
*   **`Buf` 结构体:**
    *   `buf`: 用于缓冲数据的 `Vec<u8>`。
    *   `pos`: 缓冲区中当前读取或写入位置的索引。
*   **`State<T>` 枚举:**
    *   `Idle(Option<Buf>)`: 表示 `Blocking` 处于空闲状态，并包含一个可选的 `Buf`。
    *   `Busy(sys::Blocking<(io::Result<usize>, Buf, T)>)`: 表示 `Blocking` 正在执行阻塞操作。它使用 `sys::Blocking` 在另一个线程中运行阻塞操作，并保存操作的结果、缓冲区和底层 I/O 对象。
*   **`DEFAULT_MAX_BUF_SIZE` 常量:** 定义了缓冲区大小的默认最大值。
*   **`AsyncRead` 和 `AsyncWrite` 的实现:**
    *   为 `Blocking<T>` 实现了 `AsyncRead` 和 `AsyncWrite` trait，允许在异步上下文中使用。
    *   `poll_read`: 从底层同步 `Read` 对象读取数据，并将其存储到给定的 `ReadBuf` 中。它使用一个内部缓冲区来减少阻塞操作的频率。
    *   `poll_write`: 将数据写入到底层同步 `Write` 对象。它使用一个内部缓冲区来缓冲写入的数据，并在必要时刷新缓冲区。
    *   `poll_flush`: 刷新底层同步 `Write` 对象。
    *   `poll_shutdown`: 关闭写入端。
*   **`Buf` 的方法:**
    *   `with_capacity`: 创建一个具有指定容量的 `Buf`。
    *   `is_empty`: 检查缓冲区是否为空。
    *   `len`: 返回缓冲区中未使用的字节数。
    *   `copy_to`: 将数据从缓冲区复制到 `ReadBuf`。
    *   `copy_from`: 将数据从给定的切片复制到缓冲区。
    *   `bytes`: 返回缓冲区中未使用的字节的切片。
    *   `read_from`: 从底层 `Read` 对象读取数据到缓冲区。
    *   `write_to`: 将缓冲区中的数据写入到底层 `Write` 对象。
*   **`uninterruptibly!` 宏:** 用于重复执行可能被中断的 I/O 操作。

**工作原理：**

`Blocking` 结构体通过在内部使用一个线程池来处理阻塞的 I/O 操作。当 `poll_read` 或 `poll_write` 被调用时，如果需要执行阻塞操作，它会将操作提交到线程池，并在 `State::Busy` 状态下等待结果。当操作完成时，结果将被返回，并且 `Blocking` 切换回 `State::Idle` 状态。

**与项目的关系：**

这个文件是 Tokio 运行时 I/O 模块的一部分，它允许在异步程序中使用同步 I/O 操作。它为需要与阻塞 I/O 交互的应用程序提供了便利，例如与旧版库或系统调用交互。
