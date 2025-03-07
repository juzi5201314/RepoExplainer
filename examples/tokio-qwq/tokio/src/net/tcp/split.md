# 文件说明：`tokio/src/net/tcp/split.rs`

## **文件目的**  
此文件实现了 Tokio 中 `TcpStream` 的拆分功能，允许将 TCP 连接拆分为独立的读取半部（`ReadHalf`）和写入半部（`WriteHalf`）。通过 `TcpStream::split` 方法，用户可以同时进行异步读写操作，而无需阻塞彼此。

---

## **核心组件**

### **1. `ReadHalf` 和 `WriteHalf` 结构体**
- **`ReadHalf<'a>`**  
  - 表示 `TcpStream` 的读取半部，持有对原始 `TcpStream` 的不可变引用。  
  - 实现 `AsyncRead` 特性，支持异步读取操作（如 `poll_read`、`peek`、`try_read`）。  
  - 提供 `peer_addr` 和 `local_addr` 方法获取对端和本地地址。  

- **`WriteHalf<'a>`**  
  - 表示 `TcpStream` 的写入半部，同样持有对原始 `TcpStream` 的不可变引用。  
  - 实现 `AsyncWrite` 特性，支持异步写入操作（如 `poll_write`、`try_write`）。  
  - 在 `poll_shutdown` 方法中，会关闭 TCP 连接的写方向（`Shutdown::Write`）。  

### **2. `split` 函数**
- **功能**：将 `TcpStream` 拆分为 `ReadHalf` 和 `WriteHalf`。  
- **实现**：通过 `&*stream` 将可变引用转换为不可变引用，确保拆分后的半部不会同时被修改。  
- **优势**：相比通用的 `AsyncRead + AsyncWrite` 拆分，此实现无额外开销，并通过类型系统保证线程安全。

---

## **关键方法与功能**

### **`ReadHalf` 的核心方法**
- **`poll_peek` 和 `peek`**：非阻塞预读取数据，不移除队列中的数据。  
- **`ready` 和 `readable`**：等待流变为可读状态，支持与 `try_read` 配合使用。  
- **`try_read`/`try_read_vectored`**：立即尝试读取数据，若不可读则返回 `WouldBlock`。  

### **`WriteHalf` 的核心方法**
- **`try_write`/`try_write_vectored`**：立即尝试写入数据，若不可写则返回 `WouldBlock`。  
- **`writable`**：等待流变为可写状态。  
- **`poll_shutdown`**：关闭写方向，释放资源。

---

## **与 Tokio 生态的集成**
- **异步特性实现**：  
  - `ReadHalf` 实现 `AsyncRead`，通过 `poll_read` 方法与 Tokio 的异步读取管道（如 `AsyncReadExt`）无缝衔接。  
  - `WriteHalf` 实现 `AsyncWrite`，支持 `poll_write` 和 `poll_write_vectored`，并提供 `poll_shutdown` 完成流关闭。  
- **类型安全**：  
  通过借用原始 `TcpStream`，确保拆分后的半部不会同时被多个任务修改，避免竞态条件。

---

## **文件在项目中的角色**  
此文件为 Tokio 的 TCP 网络编程提供了高效的读写拆分功能，允许开发者在异步环境中独立处理读写操作，提升并发性能，同时通过类型系统保证线程安全。
