# `split_owned.rs` 文件详解

## 目的
该文件实现了 Tokio 中 `TcpStream` 的 **独占所有权拆分功能**。通过 `TcpStream::into_split` 方法，可以将 `TcpStream` 拆分为两个独立的所有权结构 `OwnedReadHalf`（读半部）和 `OwnedWriteHalf`（写半部）。这两个结构分别实现了 `AsyncRead` 和 `AsyncWrite` 特性，允许在异步环境中独立处理读写操作，同时避免了通用拆分方法的额外开销。

---

## 核心组件

### 1. **结构体定义**
#### `OwnedReadHalf`
- **功能**：提供对 TCP 连接的只读访问。
- **实现**：
  - 内部通过 `Arc<TcpStream>` 共享对原始 `TcpStream` 的所有权。
  - 提供 `poll_peek`、`peek`、`try_read` 等方法，支持非阻塞读取和检查就绪状态。
  - 实现 `AsyncRead` 特性，允许通过 `poll_read` 进行异步读取。

#### `OwnedWriteHalf`
- **功能**：提供对 TCP 连接的只写访问。
- **实现**：
  - 内部同样通过 `Arc<TcpStream>` 共享所有权。
  - 包含 `shutdown_on_drop` 标志，确保在析构时关闭写方向（除非显式调用 `forget`）。
  - 提供 `try_write`、`poll_write` 等方法，支持非阻塞写入。
  - 实现 `AsyncWrite` 特性，并在 `poll_shutdown` 中关闭写方向。

---

### 2. **关键函数**
#### `split_owned`
- **功能**：将 `TcpStream` 拆分为 `OwnedReadHalf` 和 `OwnedWriteHalf`。
- **实现**：
  - 使用 `Arc` 包装原始 `TcpStream`，确保两个半部共享所有权。
  - 返回拆分后的两个结构体实例。

#### `reunite`
- **功能**：尝试将两个半部重新合并为原始 `TcpStream`。
- **实现**：
  - 检查两个半部是否来自同一 `TcpStream`（通过指针比较）。
  - 若成功，通过 `Arc::try_unwrap` 取回原始所有权；否则返回错误。

---

### 3. **生命周期管理**
- **`OwnedWriteHalf` 的析构**：
  - 若 `shutdown_on_drop` 为 `true`，在析构时调用 `shutdown(Shutdown::Write)` 关闭写方向。
  - 通过 `forget` 方法可禁用此行为，延迟关闭直到读半部也被丢弃。

---

### 4. **错误处理**
- **`ReuniteError`**：
  - 当尝试合并不同 `TcpStream` 的半部时抛出，携带未合并的两个半部实例。

---

## 在项目中的角色
该文件为 Tokio 的 TCP 网络编程提供了 **高效的所有权拆分机制**，允许开发者将读写操作分离到不同异步任务中，同时确保资源安全和零开销抽象。它是构建高性能网络应用（如并发服务器）的核心基础，支持独立控制读写流并简化错误处理。
