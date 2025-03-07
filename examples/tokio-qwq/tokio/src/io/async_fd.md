### 文件说明：`async_fd.rs`

#### 目的
`async_fd.rs` 是 Tokio 库中用于在 Unix 系统上实现异步 I/O 操作的核心模块。它通过 `AsyncFd` 结构体将传统的基于文件描述符（File Descriptor, FD）的 I/O 对象（如套接字、管道等）与 Tokio 的事件循环（Reactor）集成，使其支持异步读写操作。

---

#### 核心组件

1. **`AsyncFd<T>` 结构体**
   - **功能**：包装一个实现了 `AsRawFd` 的对象（如 `TcpStream`），并将其注册到 Tokio 的事件循环中。
   - **关键字段**：
     - `registration`: 负责与 Tokio 反应堆的注册和事件监听。
     - `inner`: 存储被包装的原始 I/O 对象。
   - **方法**：
     - `new`/`with_interest`: 创建 `AsyncFd` 并注册到反应堆，指定关注的事件（如可读、可写）。
     - `readable`/`writable`: 返回异步 future，等待文件描述符变为可读/可写。
     - `poll_read_ready`/`poll_write_ready`: 用于轮询式检查就绪状态，适用于不使用 future 的场景。
     - `into_inner`: 解除包装，释放原始对象并注销反应堆。

2. **`AsyncFdReadyGuard` 和 `AsyncFdReadyMutGuard`**
   - **功能**：在 I/O 操作完成后，通过这些 guard 结构体显式通知 Tokio 文件描述符的就绪状态已消耗。
   - **关键方法**：
     - `clear_ready`: 清除内部就绪标志，确保事件循环正确跟踪状态。
     - `try_io`: 尝试执行 I/O 操作，若失败则自动清除就绪状态。

3. **就绪状态管理**
   - **边缘触发（Edge-Triggered）机制**：依赖操作系统通知，仅在状态变化时触发事件。需在操作失败（如 `WouldBlock`）时手动清除状态，避免后续误判。
   - **示例**：通过 `guard.clear_ready_matching(Ready::READABLE)` 显式标记读就绪状态已处理。

---

#### 工作流程
1. **注册**：调用 `AsyncFd::new` 将文件描述符注册到 Tokio 的事件循环，指定关注的事件（如读、写）。
2. **等待就绪**：通过 `readable`/`writable` 等方法异步等待文件描述符变为就绪。
3. **执行操作**：在 guard 保护下执行实际的 I/O 操作（如读取或写入）。
4. **状态更新**：若操作因 `WouldBlock` 失败，调用 guard 的 `clear_ready` 方法通知 Tokio 重置状态。

---

#### 示例场景
```rust
// 将 TcpStream 转换为异步对象
let stream = TcpStream::connect("127.0.0.1:8080")?;
let async_stream = AsyncFd::new(stream)?;

// 异步读取数据
async fn read_data(stream: &AsyncFd<TcpStream>) {
    loop {
        let mut guard = stream.readable().await.unwrap();
        match guard.try_io(|inner| inner.read(&mut buf)) {
            Ok(Ok(n)) => println!("Read {} bytes", n),
            Ok(Err(e)) => eprintln!("Error: {}", e),
            Err(_) => continue, // WouldBlock，继续轮询
        }
    }
}
```

---

#### 在项目中的角色