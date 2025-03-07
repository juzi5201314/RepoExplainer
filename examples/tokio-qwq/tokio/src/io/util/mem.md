### 文件说明：Tokio 内存 I/O 类型实现

#### 文件路径
`explanations/tokio/tokio/src/io/util/mem.rs`

#### 文件目的
该文件实现了 Tokio 的内存 I/O 类型 `DuplexStream` 和 `SimplexStream`，提供进程内内存管道功能。通过这些类型，可以在同一进程中模拟双向或单向的异步读写操作，常用于测试或进程内通信。

---

#### 核心组件

##### 1. **DuplexStream（双向流）**
- **功能**：创建一对相互连接的内存管道，两端可同时读写。
- **结构**：
  - `read`: 读取端的 `SimplexStream` 引用（`Arc<Mutex<SimplexStream>>`）
  - `write`: 写入端的 `SimplexStream` 引用
- **创建方式**：通过 `duplex(max_buf_size)` 函数生成一对互连的 `DuplexStream`，两端的读写操作通过共享的 `SimplexStream` 实现数据传递。
- **行为**：
  - 当一端被丢弃时，另一端的读操作会读完剩余数据后返回 EOF（0 字节），写操作立即报错 `BrokenPipe`。
  - 通过 `Drop` trait 在销毁时通知另一端关闭。

##### 2. **SimplexStream（单向流）**
- **功能**：实现单向内存管道，支持读或写操作。
- **结构**：
  - `buffer`: 使用 `BytesMut` 存储数据，支持高效读写。
  - `is_closed`: 标记流是否关闭。
  - `max_buf_size`: 缓冲区最大容量，超过时写操作返回 `Pending`。
  - `read_waker`/`write_waker`: 存储等待任务的唤醒器，用于通知任务数据就绪或空间释放。
- **方法**：
  - `poll_read_internal`: 从缓冲区读取数据，若无数据则挂起任务。
  - `poll_write_internal`: 向缓冲区写入数据，若满则挂起任务。
  - `close_write`/`close_read`: 关闭流并唤醒等待任务。

##### 3. **关键函数**
- **`duplex(max_buf_size)`**：创建双向流对，内部通过 `SimplexStream` 实现互连。
- **`simplex(max_buf_size)`**：创建单向流对（读/写分离），通过 `split` 函数分割 `SimplexStream`。
- **`new_unsplit`**：初始化未分割的 `SimplexStream`，支持同时读写。

---

#### 实现细节
1. **缓冲区管理**：
   - 使用 `BytesMut` 存储数据，支持高效 `Buf` 和 `BufMut` 操作。
   - 写入时检查缓冲区容量，超过 `max_buf_size` 返回 `Pending`，并记录写任务的唤醒器。
   - 读取时若缓冲区为空且未关闭，挂起读任务并记录唤醒器。

2. **异步通知机制**：
   - 通过 `Waker` 在缓冲区状态变化时（如数据到达或空间释放）唤醒等待任务。
   - 读/写操作完成后主动唤醒对端任务，确保事件驱动的高效性。

3. **关闭行为**：
   - 调用 `close_write`/`close_read` 标记流关闭，并唤醒所有等待任务。
   - 关闭后写操作立即报错，读操作在缓冲区清空后返回 EOF。

---

#### 在项目中的角色
该文件为 Tokio 提供了轻量级的内存 I/O 实现，用于模拟网络通信或进程内高效数据传输，是测试异步 I/O 逻辑和实现内存管道的核心组件。
