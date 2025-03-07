# 文件说明：`tokio/src/net/unix/socket.rs`

## 文件目的  
该文件定义了 Tokio 异步运行时中 Unix 套接字的底层抽象 `UnixSocket`，提供对原始 Unix 套接字的直接控制能力。它允许用户在创建流、数据报或监听器之前配置套接字选项（如绑定地址、设置非阻塞模式等），适用于 Tokio 默认配置无法满足需求的场景。

---

## 核心组件与功能

### 1. **`UnixSocket` 结构体**
- **功能**：封装操作系统级的 Unix 套接字，支持配置后转换为 `UnixStream`、`UnixDatagram` 或 `UnixListener`。
- **关键属性**：
  - `inner`: 使用 `socket2` 库管理底层套接字，提供跨平台的低级控制。
- **生命周期**：当 `UnixSocket` 被丢弃时，底层套接字会被自动关闭。

### 2. **套接字创建方法**
- **`new_datagram()`**: 创建数据报套接字（`SOCK_DGRAM`），用于无连接通信。
- **`new_stream()`**: 创建流套接字（`SOCK_STREAM`），用于面向连接的通信。
- **`new(ty)`**: 内部方法，通过 `socket2::Socket::new` 创建套接字，并设置为非阻塞模式（跨平台兼容）。

### 3. **配置与绑定**
- **`bind(path)`**: 将套接字绑定到指定路径，调用系统 `bind(2)` 函数。
- **`listen(backlog)`**: 将套接字转换为监听器（需为流套接字），设置最大连接队列长度。
- **`connect(path)`**: 异步连接到指定路径的对端套接字（仅适用于流套接字），返回 `UnixStream`。

### 4. **类型转换方法**
- **`listen()`**: 转换为 `UnixListener`，用于接受传入连接。
- **`connect()`**: 转换为 `UnixStream`，用于流式通信。
- **`datagram()`**: 转换为 `UnixDatagram`，用于无连接数据报通信。

### 5. **底层交互支持**
- **`AsRawFd`/`IntoRawFd` 等 trait 实现**：允许直接访问原始文件描述符（`RawFd`），便于通过 `socket2` 或其他 crate 设置自定义套接字选项。

---

## 工作流程示例
```rust
// 创建流套接字并绑定
let socket = UnixSocket::new_stream()?;
socket.bind("/path/to/socket")?;

// 转换为监听器
let listener = socket.listen(1024)?;
```

---

## 项目中的角色  
该文件为 Tokio 的 Unix 套接字功能提供了底层配置能力，允许开发者在创建高级抽象（如 `UnixStream`）之前自定义套接字选项，是 Tokio 网络模块中灵活性与控制力的核心实现。
