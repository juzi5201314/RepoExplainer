### 代码文件解释：`tokio/src/sync/oneshot.rs`

#### **目的**
该文件实现了 Tokio 框架中的 **单次通道（oneshot channel）**，用于在异步任务之间发送单个值。通道由一对 `Sender` 和 `Receiver` 组成，支持跨任务通信，并处理发送方或接收方提前终止的情况。

---

#### **关键组件**

1. **结构体定义**
   - **`Sender<T>`**  
     发送端句柄，负责发送值。包含指向共享状态的 `Arc<Inner<T>>`，并通过原子操作管理通道状态。
     - 方法：
       - `send(T)`：同步发送值，若接收端已关闭则返回错误。
       - `closed()`：等待接收端关闭的异步方法。
       - `is_closed()`：检查接收端是否已关闭。

   - **`Receiver<T>`**  
     接收端句柄，实现 `Future` 特性，可通过 `.await` 获取值。包含共享状态引用，并支持 `try_recv()` 同步检查。
     - 方法：
       - `close()`：显式关闭接收端，阻止后续发送。
       - `try_recv()`：立即尝试获取值，不阻塞。
       - `is_terminated()`：检查是否已完成或已终止。

   - **`Inner<T>`**  
     通道的内部状态管理结构，使用原子操作和无锁技术保证线程安全：
     - `state`: 用位掩码记录通道状态（如是否已发送、是否关闭）。
     - `value`: 通过 `UnsafeCell` 存储待传递的值。
     - `tx_task` 和 `rx_task`: 存储发送/接收端的唤醒任务（Waker）。

2. **状态管理**
   - **状态位掩码**  
     `Inner` 的 `state` 字段通过位操作管理通道状态：
     - `VALUE_SENT`: 值已发送。
     - `CLOSED`: 接收端已关闭。
     - `RX_TASK_SET`/`TX_TASK_SET`: 标记是否已注册唤醒任务。

3. **错误处理**
   - `error` 模块定义了两类错误：
     - `RecvError`: 接收端因发送端关闭而失败。
     - `TryRecvError`: 同步检查时的空或关闭状态错误。

---

#### **核心功能实现**

1. **通道创建 (`channel()`)**
   - 调用 `channel()` 生成 `(Sender, Receiver)` 对，共享 `Inner<T>` 实例。
   - 初始化状态为未发送、未关闭，任务未注册。

2. **发送逻辑 (`Sender::send()`)**
   - 将值写入 `UnsafeCell`，并通过原子操作标记 `VALUE_SENT`。
   - 若接收端已关闭（`CLOSED` 标志），直接返回错误。
   - 成功发送后唤醒等待的接收端任务。

3. **接收逻辑 (`Receiver` 的 `Future` 实现)**
   - `poll()` 方法检查状态：
     - 若已发送且未关闭，取出值并返回 `Ready(Ok)`。
     - 若接收端已关闭，返回 `Ready(Err)`。
     - 否则注册当前任务的 Waker 并返回 `Pending`。

4. **任务唤醒机制**
   - 当发送或关闭操作发生时，通过 `Task` 结构体唤醒等待的对端任务。
   - 使用原子操作确保状态更新的可见性，避免竞态条件。

---

#### **使用示例**
```rust
// 创建通道
let (tx, rx) = oneshot::channel();

// 在异步任务中发送值
tokio::spawn(async move {
    tx.send(42).unwrap();
});

// 等待接收值
match rx.await {
    Ok(v) => println!("Received {}", v),
    Err(_) => eprintln!("Sender dropped"),
}
```

---

#### **项目中的角色**