# 聊天服务器代码解释

## 文件目的
该文件是一个基于 Tokio 的异步聊天服务器示例，允许 Telnet 客户端连接并实时广播消息。其设计目标是通过详细展示多个异步编程概念（如通道、共享状态管理、非阻塞 I/O 等）来教学 Tokio 的使用。

## 核心组件与流程

### 1. 主要结构
```rust
struct Shared {
    peers: HashMap<SocketAddr, Tx>, // 存储所有客户端的传输通道
}

struct Peer {
    lines: Framed<TcpStream, LinesCodec>, // 处理 TCP 流的行协议解码
    rx: Rx, // 接收其他客户端消息的通道
}
```

### 2. 核心流程
1. **服务器启动**：
   - 监听指定端口（默认 `localhost:6142`）
   - 使用 `TcpListener` 异步接受连接请求
   - 每个新连接触发独立任务处理

2. **客户端处理流程**：
   ```mermaid
   graph LR
     A[连接建立] --> B[获取用户名]
     B --> C[注册到共享状态]
     C --> D[消息循环]
     D -->|接收消息| E[广播给其他客户端]
     D -->|接收广播| F[发送到当前客户端]
     D -->|断开连接| G[移除并通知]
   ```

3. **消息广播机制**：
   - 每个客户端连接时创建无界通道 `(tx, rx)`
   - `Shared.broadcast()` 方法遍历所有客户端（排除发送者）通过 `tx` 发送消息
   - 使用 `Mutex` 保证对共享状态的线程安全访问

### 3. 关键技术点
| 技术点                | 实现细节                                                                 |
|-----------------------|--------------------------------------------------------------------------|
| 异步 I/O              | `TcpListener` 和 `Framed` 实现非阻塞 TCP 通信                              |
| 状态共享              | `Arc<Mutex<Shared>>` 提供安全的多任务共享数据访问                         |
| 消息通道              | `mpsc::unbounded_channel()` 实现客户端间消息传递                          |
| 行协议处理            | `LinesCodec` 自动处理 `\r\n` 分隔的文本消息                              |
| 任务管理              | `tokio::spawn()` 创建独立任务处理每个客户端连接                           |

### 4. 日志与错误处理
- 使用 `tracing` 库记录日志，通过环境变量 `RUST_LOG` 控制日志级别
- 错误处理采用 `?` 操作符传播错误，关键错误通过 `tracing::error` 记录

## 项目中的角色