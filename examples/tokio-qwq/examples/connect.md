### 文件说明

#### 目的
该文件是一个 Tokio 异步编程示例，演示如何将标准输入（stdin）和标准输出（stdout）与 TCP 或 UDP 网络流连接。用户可通过命令行参数指定目标地址和协议类型，实现数据的双向传输。

#### 核心组件
1. **参数解析模块**
   - 通过 `env::args` 解析命令行参数：
     - `--udp` 标志选择 UDP 模式，默认为 TCP
     - 第一个参数为必填的 `SocketAddr` 格式地址（如 `127.0.0.1:8080`）

2. **输入输出流构建**
   - 使用 `tokio_util::codec::BytesCodec` 将标准输入输出包装为异步流：
     ```rust
     let stdin = FramedRead::new(io::stdin(), BytesCodec::new());
     let stdout = FramedWrite::new(io::stdout(), BytesCodec::new());
     ```

3. **TCP 模块 (`mod tcp`)**
   - 建立 TCP 连接后分割读写流：
     ```rust
     let (r, w) = stream.split();
     ```
   - 使用 `FramedWrite` 和 `FramedRead` 处理数据流：
     - 将读取的 `BytesMut` 转换为 `Bytes` 类型
     - 异常时终止流并打印错误信息
   - 并行执行数据发送和接收：
     ```rust
     future::join(sink.send_all(&mut stdin), stdout.send_all(&mut stream))
     ```

4. **UDP 模块 (`mod udp`)**
   - 绑定本地 UDP 套接字并连接目标地址：
     ```rust
     let socket = UdpSocket::bind(bind_addr).await?;
     socket.connect(addr).await?;
     ```
   - 分离发送和接收协程：
     - `send` 协程逐行读取标准输入并发送数据包
     - `recv` 协程持续接收数据并写入标准输出：
       ```rust
       loop {
           let mut buf = vec![0; 1024];
           let n = reader.recv(&mut buf[..]).await?;
           if n > 0 {
               stdout.send(Bytes::from(buf)).await?;
           }
       }
       ```

#### 项目中的角色