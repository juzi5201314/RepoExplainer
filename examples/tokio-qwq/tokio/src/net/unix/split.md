# `split.rs` 文件详解

## 文件目的
该文件为 Tokio 的 Unix 域套接字（`UnixStream`）提供了异步读写分离功能。通过 `UnixStream::split` 方法，可将一个 `UnixStream` 分割为独立的读取半部（`ReadHalf`）和写入半部（`WriteHalf`），分别实现 `AsyncRead` 和 `AsyncWrite` trait，从而在异步编程中实现非阻塞的独立读写操作。

---

## 核心组件

### 1. **结构体定义**
- **`ReadHalf<'a>`**  
  - 类型：`struct ReadHalf<'a>(&'a UnixStream)`  
  - 功能：持有对原始 `UnixStream` 的不可变引用，提供异步读取能力。  
  - 特性：  
    - 实现 `AsyncRead` trait，支持 `poll_read` 方法。  
    - 提供 `try_read`、`try_read_buf` 等非阻塞读取方法。  
    - 提供 `peer_addr` 和 `local_addr` 获取套接字地址信息。

- **`WriteHalf<'a>`**  
  - 类型：`struct WriteHalf<'a>(&'a UnixStream)`  
  - 功能：持有对原始 `UnixStream` 的不可变引用，提供异步写入能力。  
  - 特性：  
    - 实现 `AsyncWrite` trait，支持 `poll_write`、`poll_shutdown` 方法。  
    - 提供 `try_write`、`try_write_vectored` 等非阻塞写入方法。  
    - `poll_shutdown` 方法会关闭写方向（`Shutdown::Write`）。  
    - 同样支持地址查询方法。

---

### 2. **关键方法**
#### `split` 函数
- **功能**：将 `UnixStream` 分割为 `ReadHalf` 和 `WriteHalf`。  
- **实现**：  
  ```rust
  pub(crate) fn split(stream: &mut UnixStream) -> (ReadHalf<'_>, WriteHalf<'_>) {
      (ReadHalf(stream), WriteHalf(stream))
  }
  ```
- **特点**：  
  - 零开销分割，直接通过引用共享底层资源。  
  - 通过类型系统确保读写操作互不干扰。

#### 异步操作方法
- **读操作**：  
  - `ready(interest)`：检查套接字是否就绪（支持 `Interest::READABLE` 或 `Interest::WRITE_CLOSED`）。  
  - `readable()`：等待可读状态。  
  - `try_read`：非阻塞读取数据到缓冲区。  

- **写操作**：  
  - `writable()`：等待可写状态。  
  - `try_write`：非阻塞写入数据到套接字。  
  - `poll_shutdown`：关闭写方向，实现 `AsyncWrite` 的关闭逻辑。

---

### 3. **Trait 实现**
- **`AsyncRead` for `ReadHalf`**  
  - 通过 `poll_read` 方法实现异步读取，调用底层 `UnixStream` 的 `poll_read_priv`。  

- **`AsyncWrite` for `WriteHalf`**  
  - 通过 `poll_write` 和 `poll_write_vectored` 实现异步写入。  
  - `poll_shutdown` 调用 `UnixStream.shutdown_std(Shutdown::Write)` 关闭写方向。  
  - `poll_flush` 直接返回成功（Unix 套接字无需显式刷新）。  

---

## 在项目中的角色
该文件为 Tokio 的 Unix 域套接字提供了高效的异步读写分离功能，通过类型安全的引用共享和零开销设计，允许开发者在异步任务中独立处理读写操作，提升并发性能并避免竞态条件。它是 Tokio 异步 I/O 框架中 Unix 域套接字支持的重要组成部分。
