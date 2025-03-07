# 代码文件解释：`tokio/src/net/windows/named_pipe.rs`

## **目的**
该文件为 Tokio 提供了对 Windows 命名管道（Named Pipes）的异步支持。它实现了服务器端和客户端的命名管道操作，允许在异步环境中进行非阻塞的读写、连接管理和配置设置。

---

## **关键组件**

### **1. 命名管道服务器 (`NamedPipeServer`)**
- **功能**：管理服务器端的命名管道实例，监听客户端连接并处理 I/O 操作。
- **核心方法**：
  - `connect()`: 异步等待客户端连接。
  - `disconnect()`: 断开当前客户端连接。
  - `ready()`/`poll_read_ready()`/`poll_write_ready()`: 检查管道的读写就绪状态。
  - `try_read()`/`try_write()`: 非阻塞读写操作。
  - `info()`: 获取管道配置信息（如模式、缓冲区大小等）。

### **2. 命名管道客户端 (`NamedPipeClient`)**
- **功能**：管理客户端与服务器的连接，执行读写操作。
- **核心方法**：
  - `open()`: 连接到服务器端的命名管道。
  - `try_read()`/`try_write()`: 非阻塞读写操作。
  - `ready()`/`poll_read_ready()`/`poll_write_ready()`: 检查管道的读写就绪状态。

### **3. 配置构建器**
- **服务器配置 (`ServerOptions`)**：
  - 设置管道访问权限（如双向通信、只读或只写）。
  - 配置缓冲区大小、最大实例数、安全属性等。
  - 示例：`ServerOptions::new().access_inbound(true).create(pipe_name)`。

- **客户端配置 (`ClientOptions`)**：
  - 控制客户端的读写权限。
  - 设置安全标识（如 `security_qos_flags`）。
  - 示例：`ClientOptions::new().read(false).open(pipe_name)`。

### **4. 管道信息 (`PipeInfo`)**
- **功能**：通过 `info()` 方法获取管道的运行时配置，包括：
  - `mode`: 字节流或消息模式 (`PipeMode::Byte`/`PipeMode::Message`)。
  - `end`: 管道的端点 (`PipeEnd::Server`/`PipeEnd::Client`)。
  - 缓冲区大小和最大实例数。

### **5. 安全与系统调用**
- **Ffi 调用**：通过 `unsafe` 块调用 Windows API（如 `CreateNamedPipe`、`ConnectNamedPipe`）。
- **资源管理**：确保句柄（handle）的正确释放和所有权转移，避免资源泄漏。

---

## **使用模式与示例**
### **服务器端示例**
```rust
let server = ServerOptions::new()
    .max_instances(5)
    .create(PIPE_NAME)?;
loop {
    server.connect().await?;
    let client = server; // 接受连接后转移所有权
    // 创建新服务器实例以保持可用性
    server = ServerOptions::new().create(PIPE_NAME)?;
    tokio::spawn(handle_client(client));
}
```

### **客户端示例**
```rust
loop {
    match ClientOptions::new().open(PIPE_NAME) {
        Ok(client) => break,
        Err(e) if e.kind() == io::ErrorKind::NotFound => {
            // 服务器未启动，重试或处理错误
        },
        Err(e) if e.raw_os_error() == Some(ERROR_PIPE_BUSY) => {
            // 等待服务器就绪
            tokio::time::sleep(Duration::from_millis(50)).await;
        },
        Err(e) => return Err(e),
    }
}
```

---

## **项目中的角色**
该文件为 Tokio 提供了 **Windows 命名管道的异步接口**，支持服务器和客户端的创建、连接管理、安全配置以及非阻塞 I/O 操作。它通过封装 Windows 系统调用，为 Rust 异步生态提供了跨平台友好的命名管道实现，适用于需要进程间通信（IPC）或远程服务调用的场景。
