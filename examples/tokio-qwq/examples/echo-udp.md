# UDP回显服务器代码解析

## 代码目的
该文件实现了一个基于Tokio异步运行时的UDP回显服务器。服务器接收客户端发送的数据包后，立即将其内容原样返回给发送方。作为Tokio框架的示例程序，用于演示异步UDP编程的基本模式。

## 关键组件

### 1. Server结构体
```rust
struct Server {
    socket: UdpSocket,
    buf: Vec<u8>,
    to_send: Option<(usize, SocketAddr)>,
}
```
- **socket**：Tokio的UDP套接字句柄，负责网络通信
- **buf**：1KB大小的字节缓冲区（`vec![0; 1024]`），用于接收数据
- **to_send**：待发送的数据长度和客户端地址元组，使用Option类型表示可能为空

### 2. 异步运行逻辑（run方法）
```rust
async fn run(self) -> Result<(), io::Error> {
    loop {
        // 发送阶段
        if let Some((size, peer)) = to_send {
            let amt = socket.send_to(&buf[..size], &peer).await?;
            println!("Echoed {amt}/{size} bytes to {peer}");
        }

        // 接收阶段
        to_send = Some(socket.recv_from(&mut buf).await?);
    }
}
```
- **循环机制**：无限循环处理UDP数据包
- **发送逻辑**：优先处理待发送的数据包（`to_send`），通过`send_to`异步发送
- **接收逻辑**：使用`recv_from`异步接收新数据包，将结果存入`to_send`供下次循环处理

### 3. 主函数（main）
```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr = env::args().nth(1).unwrap_or_else(|| "127.0.0.1:8080".to_string());
    let socket = UdpSocket::bind(&addr).await?;
    let server = Server { socket, buf: vec![0; 1024], to_send: None };
    server.run().await?;
    Ok(())
}
```
- **参数处理**：从命令行获取绑定地址，缺省使用本地8080端口
- **套接字绑定**：通过`UdpSocket::bind`异步绑定地址
- **启动服务**：创建Server实例并启动异步运行循环

## 实现原理
1. 使用Tokio的异步UDP套接字实现非阻塞IO
2. 通过循环交替处理发送和接收操作：
   - 先完成待发送的数据包
   - 再接收新数据包到缓冲区
3. 利用`send_to`和`recv_from`的异步特性，保持事件循环的高效运行

## 项目角色