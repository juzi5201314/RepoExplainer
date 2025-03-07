# 文件说明：`tokio/src/net/unix/split_owned.rs`

## **功能与目的**  
该文件实现了 Tokio 中 `UnixStream` 的 **所有权拆分功能**，将一个 Unix 域套接字流拆分为独立的读取半部 (`OwnedReadHalf`) 和写入半部 (`OwnedWriteHalf`)。这种拆分允许在异步环境中对读写操作进行独立控制，同时避免了通用拆分方法的性能开销，并通过类型系统保证了操作的安全性。

---

## **核心组件**

### **1. `OwnedReadHalf` 和 `OwnedWriteHalf` 结构体**
- **数据结构**：
  - 两者均通过 `Arc<UnixStream>` 共享底层套接字资源。
  - `OwnedWriteHalf` 还包含 `shutdown_on_drop` 标志，控制在析构时是否关闭写入方向。
- **功能差异**：
  - **读半部 (`OwnedReadHalf`)**：
    - 实现 `AsyncRead`，支持非阻塞读取操作（如 `try_read`、`try_read_buf`）。
    - 提供 `peer_addr` 和 `local_addr` 获取套接字地址。
  - **写半部 (`OwnedWriteHalf`)**：
    - 实现 `AsyncWrite`，支持非阻塞写入操作（如 `try_write`、`try_write_vectored`）。
    - 在析构时默认关闭写入方向，但可通过 `forget` 方法延迟关闭。

### **2. 拆分与合并函数**
- **`split_owned`**：
  - 将 `UnixStream` 拆分为两个半部，通过 `Arc` 实现资源共享。
- **`reunite`**：
  - 尝试将两个半部重新合并为原始 `UnixStream`。若半部来自不同拆分，返回 `ReuniteError`。

### **3. 错误处理**
- **`ReuniteError`**：
  - 当尝试合并来自不同套接字的半部时抛出，包含无效的读写半部实例。

---

## **关键实现细节**
1. **所有权与共享**：
   - 使用 `Arc` 确保两个半部安全共享底层套接字，避免借用检查器限制。
   - 与非所有权拆分（如 `split` 方法）不同，`into_split` 返回的半部无需借用原始流，支持更灵活的并发操作。

2. **异步 I/O 支持**：
   - `AsyncRead` 和 `AsyncWrite` 特性通过 `poll_read`、`poll_write` 等方法实现，直接调用底层套接字的私有方法。
   - 写半部的 `poll_shutdown` 方法显式关闭写方向，而析构时的 `Drop` 特性自动触发关闭（除非调用 `forget`）。

3. **取消安全（Cancel-Safe）**：
   - `ready`、`readable`、`writable` 等异步方法确保在取消后仍能正确处理就绪事件。

---

## **在项目中的角色**