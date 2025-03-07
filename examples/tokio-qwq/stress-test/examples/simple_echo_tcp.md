rust
//! Simple TCP echo server to check memory leaks using Valgrind.
use std::{thread::sleep, time::Duration};

use tokio::{
    io::{AsyncReadExt, AsyncWriteExt},
    net::{TcpListener, TcpSocket},
    runtime::Builder,
    sync::oneshot,
};

const TCP_ENDPOINT: &str = "127.0.0.1:8080";
const NUM_MSGS: usize = 100;
const MSG_SIZE: usize = 1024;

fn main() {
    let rt = Builder::new_multi_thread().enable_io().build().unwrap();
    let rt2 = Builder::new_multi_thread().enable_io().build().unwrap();

    rt.spawn(async {
        let listener = TcpListener::bind(TCP_ENDPOINT).await.unwrap();
        let (mut socket, _) = listener.accept().await.unwrap();
        let (mut rd, mut wr) = socket.split();
        while tokio::io::copy(&mut rd, &mut wr).await.is_ok() {}
    });

    sleep(Duration::from_millis(100));

    let (tx, mut rx) = oneshot::channel();

    rt2.spawn(async {
        let addr = TCP_ENDPOINT.parse().unwrap();
        let socket = TcpSocket::new_v4().unwrap();
        let mut stream = socket.connect(addr).await.unwrap();

        let mut buff = [0; MSG_SIZE];
        for _ in 0..NUM_MSGS {
            let one_mega_random_bytes: Vec<u8> =
                (0..MSG_SIZE).map(|_| rand::random::<u8>()).collect();
            stream.write_all(one_mega_random_bytes.as_slice()).await.unwrap();
            let _ = stream.read(&mut buff).await.unwrap();
        }
        tx.send(()).unwrap();
    });

    loop {
        match rx.try_recv() {
            Err(oneshot::error::TryRecvError::Empty) => (),
            Err(oneshot::error::TryRecvError::Closed) => panic!("channel got closed..."),
            Ok(()) => break,
        }
    }
}
```

---

### 代码文件解释

#### **目的**
该文件是一个简单的 TCP 回声服务器，用于通过 **Valgrind** 检测内存泄漏。它通过模拟高负载场景（发送和接收大量数据包）来测试 Tokio 异步运行时的内存管理稳定性。

---

#### **关键组件**

1. **运行时配置 (`Builder::new_multi_thread`)**  
   - 创建了两个独立的 Tokio 运行时 (`rt` 和 `rt2`)，分别用于服务器和客户端逻辑。  
   - `enable_io()` 启用 I/O 支持，`multi_thread` 允许多线程并发处理任务。

2. **服务器端逻辑**  
   - **绑定端口**：通过 `TcpListener::bind` 监听 `127.0.0.1:8080`。  
   - **拆分套接字 (`split`)**：将 TCP 套接字拆分为读 (`rd`) 和写 (`wr`) 两个异步流，允许并发读写。  
   - **数据回传**：使用 `tokio::io::copy` 将接收到的数据直接返回客户端，实现回声功能。

3. **客户端逻辑**  
   - **连接服务器**：通过 `TcpSocket::connect` 连接到服务器端口。  
   - **发送/接收数据**：循环发送 `NUM_MSGS`（默认 100）次随机生成的 `MSG_SIZE`（默认 1KB）字节数据，并等待响应。  
   - **通道同步 (`oneshot`)**：通过 `oneshot` 通道通知主进程客户端任务完成。

4. **同步与超时处理**  
   - **等待绑定 (`sleep`)**：主线程休眠 100ms，确保服务器端口成功绑定后再启动客户端。  
   - **循环检查通道**：通过 `rx.try_recv()` 检查客户端是否完成，若未完成则循环等待，若通道关闭则触发 panic。

---

#### **代码流程**
1. 启动服务器运行时 (`rt`)，监听端口并等待连接。  
2. 主线程休眠 100ms，确保服务器就绪。  
3. 启动客户端运行时 (`rt2`)，连接服务器并发送/接收数据。  
4. 客户端完成后通过 `oneshot` 通道通知主进程。  
5. 主进程收到信号后退出循环，结束程序。

---

#### **项目中的角色**