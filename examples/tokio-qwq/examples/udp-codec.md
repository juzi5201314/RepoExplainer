rust
//! 这个示例使用 `BytesCodec` 创建了一个基于自定义协议的 UDP 客户端和服务器，并实现了一个“ping-pong”交互。

#![warn(rust_2018_idioms)]

use tokio::net::UdpSocket;
use tokio::{io, time};
use tokio_stream::StreamExt;
use tokio_util::codec::BytesCodec;
use tokio_util::udp::UdpFramed;

use bytes::Bytes;
use futures::{FutureExt, SinkExt};
use std::env;
use std::error::Error;
use std::net::SocketAddr;
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // 解析命令行参数或使用默认地址
    let addr = env::args().nth(1).unwrap_or_else(|| "127.0.0.1:0".to_string());

    // 绑定两个 UDP 套接字并获取它们的本地地址
    let a = UdpSocket::bind(&addr).await?;
    let b = UdpSocket::bind(&addr).await?;
    let b_addr = b.local_addr()?;

    // 使用 BytesCodec 将套接字转换为消息流
    let mut a = UdpFramed::new(a, BytesCodec::new());
    let mut b = UdpFramed::new(b, BytesCodec::new());

    // 启动两个异步任务：发送 ping 和接收 pong
    let a_task = ping(&mut a, b_addr);
    let b_task = pong(&mut b);

    // 并发执行两个任务，处理错误
    match tokio::try_join!(a_task, b_task) {
        Err(e) => println!("发生错误: {e:?}"),
        _ => println!("完成！"),
    }

    Ok(())
}

// 发送 ping 消息并等待响应
async fn ping(
    socket: &mut UdpFramed<BytesCodec>,
    b_addr: SocketAddr,
) -> Result<(), io::Error> {
    // 初始发送 PING 到地址 b
    socket.send((Bytes::from(&b"PING"[..]), b_addr)).await?;

    // 循环发送和接收 4 次
    for _ in 0..4 {
        let (bytes, addr) = socket.next().map(|e| e.unwrap()).await?;
        println!("[a] 接收: {}", String::from_utf8_lossy(&bytes));
        socket.send((Bytes::from(&b"PING"[..]), addr)).await?;
    }
    Ok(())
}

// 接收消息并回复 pong
async fn pong(socket: &mut UdpFramed<BytesCodec>) -> Result<(), io::Error> {
    let timeout = Duration::from_millis(200);
    // 循环监听消息，超时后停止
    while let Ok(Some(Ok((bytes, addr)))) = time::timeout(timeout, socket.next()).await {
        println!("[b] 接收: {}", String::from_utf8_lossy(&bytes));
        socket.send((Bytes::from(&b"PONG"[..]), addr)).await?;
    }
    Ok(())
}
```

### 代码解析

#### **核心功能**
该文件演示了如何使用 Tokio 的异步 UDP 编解码功能实现一个简单的客户端-服务器通信模型。通过 `BytesCodec` 将原始 UDP 套接字转换为消息流，实现基于文本的 "PING-PONG" 协议交互。

---

#### **关键组件**
1. **`UdpFramed` 和 `BytesCodec`**
   - `UdpFramed` 将 UDP 套接字包装为流（Stream）和汇（Sink），简化消息处理。
   - `BytesCodec` 负责将字节数据与 `(Bytes, SocketAddr)` 地址对进行编解码，避免手动处理网络字节流。

2. **`ping` 函数**
   - 发送初始 "PING" 消息到服务器地址 `b_addr`。
   - 循环接收响应并再次发送 "PING"，共执行 4 次。
   - 使用 `socket.next()` 从流中读取消息，`socket.send()` 发送回复。

3. **`pong` 函数**
   - 持续监听消息，超时（200ms）后停止。
   - 接收 "PING" 消息后打印内容，并回复 "PONG" 到发送方地址。

4. **主函数逻辑**
   - 绑定两个 UDP 套接字到本地随机端口，获取服务器地址 `b_addr`。
   - 启动 `ping` 和 `pong` 两个异步任务，通过 `tokio::try_join!` 并发执行。

---

#### **项目中的角色**
该文件是 Tokio 的 UDP 编解码示例，展示了如何通过 `UdpFramed` 和 `BytesCodec` 将 UDP 套接字转换为消息流，实现基于自定义协议的异步通信。它为开发者提供了使用 Tokio 处理 UDP 协议的模板，尤其适用于需要封装底层字节流的场景。
