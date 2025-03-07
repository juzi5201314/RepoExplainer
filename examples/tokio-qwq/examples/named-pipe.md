rust
# 代码文件解释：tokio/examples/named-pipe.rs

## 文件目的
该文件是一个 Tokio 框架的示例程序，演示如何在 Windows 系统上使用异步编程实现命名管道（Named Pipe）的客户端-服务端通信。通过异步任务并行执行，展示了如何创建管道、建立连接、发送/接收数据，并验证通信结果。

---

## 核心组件与流程

### 1. **条件编译与平台限制**
```rust
#[cfg(windows)]
```
- 仅在 Windows 系统下编译，因为命名管道是 Windows 特有的功能。
- 非 Windows 系统运行时会直接输出提示信息。

---

### 2. **服务端逻辑 (`windows_main` 函数)**
#### (1) **创建命名管道**
```rust
let server = ServerOptions::new().create(PIPE_NAME)?;
```
- 使用 `ServerOptions` 创建名为 `\\.\pipe\named-pipe-single-client` 的命名管道。
- `create` 方法会尝试创建新管道，若已存在则返回错误。

#### (2) **异步服务端任务**
```rust
let server = tokio::spawn(async move {
    server.connect().await?; // 等待客户端连接
    let mut server = BufReader::new(server);
    let mut buf = String::new();
    server.read_line(&mut buf).await?; // 读取客户端发送的 "ping\n"
    server.write_all(b"pong\n").await?; // 发送响应 "pong\n"
    Ok(buf)
});
```
- 通过 `connect().await` 非阻塞等待客户端连接。
- 使用 `BufReader` 缓冲读取，逐行解析输入。
- 读取客户端消息后，立即写回响应。

---

### 3. **客户端逻辑**
```rust
let client = tokio::spawn(async move {
    let client = ClientOptions::new().open(PIPE_NAME)?; // 连接到现有管道
    let mut client = BufReader::new(client);
    client.write_all(b"ping\n").await?; // 发送 "ping\n"
    client.read_line(&mut buf).await?; // 等待服务端响应
    Ok(buf)
});
```
- 使用 `ClientOptions` 连接服务端创建的命名管道。
- 发送文本 `ping\n`，并等待服务端的 `pong\n` 响应。

---

### 4. **任务协调与验证**
```rust
let (server, client) = tokio::try_join!(server, client)?;
assert_eq!(server?, "ping\n");
assert_eq!(client?, "pong\n");
```
- 使用 `try_join!` 同时等待服务端和客户端任务完成。
- 验证服务端收到的输入是否为 `ping\n`，客户端收到的响应是否为 `pong\n`。

---

### 5. **主函数入口**
```rust
#[tokio::main]
async fn main() -> io::Result<()> {
    #[cfg(windows)] { windows_main().await? }
    #[cfg(not(windows))] { println!("Named pipes are only supported on Windows!") }
    Ok(())
}
```
- 使用 `tokio::main` 宏启用异步主函数。
- 根据平台条件执行对应逻辑。

---

## 项目中的角色