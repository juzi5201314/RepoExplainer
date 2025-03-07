### 文件解释：`tokio-util/src/codec/framed_write.rs`

#### **目的**  
该文件实现了 `FramedWrite` 结构体，这是一个基于编码器（Encoder）的异步写入 Sink。它将待发送的数据帧通过编码器转换为字节流，并异步写入到底层的 `AsyncWrite`（如 TCP 连接或文件流）。其核心功能包括：
- 自动管理编码和缓冲区
- 处理异步写入的暂停与恢复
- 提供流量控制（backpressure）机制

---

#### **关键组件**

1. **结构体定义**  
   ```rust
   pub struct FramedWrite<T, E> {
       #[pin]
       inner: FramedImpl<T, E, WriteFrame>,
   }
   ```
   - **`inner`**：内部状态机 `FramedImpl`，包含：
     - `inner`: 底层的 `AsyncWrite` 实现（如 TcpStream）
     - `codec`: 编码器（实现 `Encoder` trait）
     - `state`: 写入状态（`WriteFrame` 枚举，跟踪编码和写入阶段）

2. **核心方法**  
   - **`new`**: 创建 `FramedWrite` 实例，初始化编码器和缓冲区。
   - **Sink 实现**:
     - `poll_ready()`: 检查是否可以发送新数据（缓冲区未满）。
     - `start_send()`: 将数据帧编码为字节并存入缓冲区。
     - `poll_flush()`: 强制将缓冲区数据写入底层流。
     - `poll_close()`: 完成写入并关闭流。
   - **缓冲区管理**:
     - `write_buffer()`: 获取当前缓冲区的只读引用。
     - `set_backpressure_boundary()`: 设置缓冲区大小阈值，超过时暂停发送新数据。

3. **状态与流量控制**  
   - **`WriteFrame` 状态机**：跟踪写入的三个阶段：
     1. 等待编码（数据帧 → 字节缓冲）
     2. 等待写入（将缓冲字节异步写入流）
     3. 完成或错误处理
   - **Backpressure 边界**：通过 `backpressure_boundary` 控制缓冲区大小，避免内存溢出。

---

#### **与其他组件的交互**  
- **依赖关系**：
  - `FramedImpl`: 内部状态机，处理编码、写入和状态转换。
  - `Encoder`: 负责将逻辑数据帧转换为字节流（如 Protobuf 编码）。
  - `AsyncWrite`: 底层异步写入目标（如 Tokio 的 TcpStream）。

- **与 `FramedRead` 的关系**：
  - `FramedWrite` 是 `Framed` 结构的写入部分，而 `FramedRead` 负责读取和解码。两者共同构成完整的 `Framed`，用于双向通信。

---

#### **使用场景**  
典型用法如下：
```rust
let (mut tx, rx) = tokio::io::duplex(1024);
let mut framed = FramedWrite::new(tx, MyEncoder {});

// 发送数据帧
framed.send(MyFrame { data: "Hello" }).await?;
// 强制刷新缓冲区
framed.flush().await?;
```

---

#### **在项目中的角色**  