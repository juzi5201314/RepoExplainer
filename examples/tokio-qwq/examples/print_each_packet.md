### 代码文件解释：`explanations/tokio/examples/print_each_packet.rs`

#### **功能与目的**
该文件是一个基于 Tokio 框架实现的简单 TCP 服务器示例，其核心功能是：
1. 监听指定端口（默认 `127.0.0.1:8080`）接收 TCP 连接。
2. 对每个连接接收到的数据包进行实时打印输出。
3. 通过 Tokio 的异步运行时实现多连接的并发处理。

#### **关键组件与实现细节**
1. **依赖与配置**
   - 使用 `tokio` 的 `TcpListener`、`StreamExt` 和 `BytesCodec` 处理网络通信和流式数据。
   - 通过 `env` 模块读取命令行参数，允许自定义监听地址。

2. **主函数逻辑**
   ```rust
   #[tokio::main]
   async fn main() -> Result<(), Box<dyn std::error::Error>> {
       // ...
   }
   ```
   - 使用 `tokio::main` 宏启动异步主函数，集成 Tokio 运行时。
   - 通过 `env::args()` 获取监听地址参数，若未指定则默认 `127.0.0.1:8080`。

3. **TCP 监听器创建**
   ```rust
   let listener = TcpListener::bind(&addr).await?;
   ```
   - 绑定地址并启动监听，异步等待连接请求。

4. **连接处理循环**
   ```rust
   loop {
       let (socket, _) = listener.accept().await?;
       tokio::spawn(async move { /* 处理连接的异步任务 */ });
   }
   ```
   - 进入无限循环，通过 `accept()` 异步接收新连接。
   - 每个连接通过 `tokio::spawn` 创建独立的异步任务，实现并发处理。

5. **数据读取与打印**
   ```rust
   let mut framed = BytesCodec::new().framed(socket);
   while let Some(message) = framed.next().await {
       match message {
           Ok(bytes) => println!("bytes: {bytes:?}"),
           Err(err) => println!("Socket closed with error: {err:?}"),
       }
   }
   ```
   - 使用 `BytesCodec` 将 TCP Socket 封装为流（`framed`），逐条读取数据包。
   - 成功读取时打印字节内容，错误时记录异常信息。
   - 流结束时（如客户端关闭连接）打印关闭信息。

#### **与项目其他部分的关联**
- **对比其他示例**：此文件与仓库中的其他示例（如 `connect` 客户端或 Echo 服务器）配合使用，验证功能。例如：
  - 客户端通过 `cargo run --example connect 127.0.0.1:8080` 连接服务器并发送数据。
  - 服务器将接收到的数据实时打印到控制台。
- **Tokio 框架特性**：展示了 Tokio 的异步并发模型，通过线程池和任务调度实现高效处理多连接。

#### **文件在项目中的角色**