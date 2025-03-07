这个文件定义了 `TcpStream` 的所有权分离支持，允许将一个 `TcpStream` 分割成 `OwnedReadHalf` 和 `OwnedWriteHalf`，分别实现 `AsyncRead` 和 `AsyncWrite` 特征。 这种分离没有相关的开销，并在类型级别强制执行所有不变性。

关键组件：

*   `OwnedReadHalf`：拥有 `TcpStream` 读半部分的结构体，实现了 `AsyncRead` 特征。
*   `OwnedWriteHalf`：拥有 `TcpStream` 写半部分的结构体，实现了 `AsyncWrite` 特征。当 `OwnedWriteHalf` 被丢弃时，会关闭 TCP 流的写方向。
*   `split_owned(stream: TcpStream) -> (OwnedReadHalf, OwnedWriteHalf)`：将 `TcpStream` 分割成 `OwnedReadHalf` 和 `OwnedWriteHalf` 的函数。
*   `reunite(read: OwnedReadHalf, write: OwnedWriteHalf) -> Result<TcpStream, ReuniteError>`：尝试将 `OwnedReadHalf` 和 `OwnedWriteHalf` 重新组合成原始的 `TcpStream`。只有当两个半部分来自同一个 `TcpStream` 时，才能成功。
*   `ReuniteError`：当尝试重新组合来自不同 socket 的两个半部分时发生的错误。
