这段代码文件实现了将一个同时实现了 `AsyncRead` 和 `AsyncWrite` 特质的类型拆分成独立的 `AsyncRead` 和 `AsyncWrite` 句柄的功能。这允许并发地进行读写操作，而无需手动管理同步。

**主要组成部分：**

*   **`ReadHalf<T>`**:  表示可读端，实现了 `AsyncRead` 特质。它持有对原始流的内部 `Inner` 结构的引用。
*   **`WriteHalf<T>`**: 表示可写端，实现了 `AsyncWrite` 特质。它也持有对原始流的内部 `Inner` 结构的引用。
*   **`Inner<T>`**:  一个内部结构，包含对原始流的 `Mutex` 保护。`Mutex` 用于确保在 `ReadHalf` 和 `WriteHalf` 之间安全地访问底层流。它还存储了 `is_write_vectored` 标志，用于指示底层流是否支持向量写操作。
*   **`split<T>(stream: T) -> (ReadHalf<T>, WriteHalf<T>)`**:  核心函数，它接收一个实现了 `AsyncRead + AsyncWrite` 的流，并返回一个 `ReadHalf` 和一个 `WriteHalf`。它使用 `Arc` 和 `Mutex` 来安全地共享底层流。
*   **`ReadHalf::unsplit(self, wr: WriteHalf<T>) -> T`**:  将 `ReadHalf` 和对应的 `WriteHalf` 重新组合成原始的流。  在调用此方法之前，必须确保 `ReadHalf` 和 `WriteHalf` 是由同一个 `split` 操作产生的。
*   **`is_pair_of(&self, other: &WriteHalf<T>) -> bool` 和 `WriteHalf::is_pair_of(&self, other: &ReadHalf<T>) -> bool`**:  用于检查 `ReadHalf` 和 `WriteHalf` 是否来自同一个 `split` 操作。
*   **`AsyncRead` 和 `AsyncWrite` 的实现**:  `ReadHalf` 实现了 `AsyncRead` 特质，`WriteHalf` 实现了 `AsyncWrite` 特质。这些实现通过获取 `Mutex` 锁来委托给底层的流进行实际的读写操作。

**工作原理：**

1.  `split` 函数接收一个实现了 `AsyncRead + AsyncWrite` 的流。
2.  它创建一个 `Inner` 结构，该结构包含对原始流的 `Mutex` 保护。
3.  它创建 `ReadHalf` 和 `WriteHalf` 结构，它们都持有对 `Inner` 结构的 `Arc` 引用。
4.  `ReadHalf` 和 `WriteHalf` 的 `AsyncRead` 和 `AsyncWrite` 实现通过获取 `Mutex` 锁来访问底层流。
5.  `unsplit` 函数通过尝试获取 `Arc` 的所有权来恢复原始流。如果 `ReadHalf` 和 `WriteHalf` 是由同一个 `split` 操作产生的，则可以成功获取所有权，并返回原始流。

**与其他文件的关系：**

这个文件定义了 `split` 功能，这对于在 Tokio 中进行并发 I/O 操作非常重要。它被其他模块使用，例如，用于将一个连接拆分成读写两端，以便可以同时进行读写操作。
