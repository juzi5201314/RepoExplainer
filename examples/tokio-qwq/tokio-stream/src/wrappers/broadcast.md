### 文件说明：`tokio-stream/src/wrappers/broadcast.rs`

#### 目的
该文件实现了 `BroadcastStream` 结构体，将 Tokio 的 `broadcast::Receiver` 类型包装为符合 `futures_core::Stream` trait 的异步流。其核心目标是让广播接收器能够通过流式接口（如 `next().await`）方便地异步消费消息。

---

#### 关键组件

1. **结构体定义**
   ```rust
   pub struct BroadcastStream<T> {
       inner: ReusableBoxFuture<'static, (Result<T, RecvError>, Receiver<T>)>,
   }
   ```
   - 使用 `ReusableBoxFuture` 存储异步任务，避免重复创建 future 对象，提升性能。
   - 内部 future 返回 `(消息结果, 更新后的接收器)` 元组，确保状态正确传递。

2. **错误类型**
   ```rust
   pub enum BroadcastStreamRecvError {
       Lagged(u64),
   }
   ```
   - 封装 Tokio 广播通道的 `RecvError`，将 `Lagged` 错误转换为自定义类型，提供更清晰的错误处理。

3. **核心方法**
   - **`new` 方法**：
     ```rust
     pub fn new(rx: Receiver<T>) -> Self {
         Self { inner: ReusableBoxFuture::new(make_future(rx)) }
     }
     ```
     初始化 future，包装 `make_future` 异步函数执行消息接收操作。

   - **`poll_next` 实现**：
     ```rust
     fn poll_next(...) -> Poll<Option<Self::Item>> {
         // 轮询 future 并处理结果
         match result {
             Ok(item) => Poll::Ready(Some(Ok(item))),
             Err(RecvError::Closed) => Poll::Ready(None),
             Err(RecvError::Lagged(n)) => Poll::Ready(Some(Err(...))),
         }
     }
     ```
     - 处理三种情况：正常消息、通道关闭、接收滞后。
     - 使用 `ReusableBoxFuture::set` 复用 future 对象。

4. **Trait 实现**
   - `Stream` trait：使 `BroadcastStream` 支持流式操作。
   - `From<Receiver<T>>`：允许直接通过 `Receiver` 构造流。
   - `Debug`：提供基本调试信息。

---

#### 工作原理
1. **Future 复用机制**：
   - `ReusableBoxFuture` 存储异步任务，每次轮询完成后通过 `set` 方法重置 future，避免重复分配内存。
   - `make_future` 函数封装 `rx.recv().await` 操作，返回结果和更新后的接收器。

2. **错误处理**：
   - `RecvError::Closed` 表示通道关闭，流结束返回 `None`。
   - `RecvError::Lagged` 转换为自定义的 `BroadcastStreamRecvError::Lagged`，保留滞后消息数量信息。

3. **流式接口适配**：
   - 通过 `poll_next` 方法实现 `Stream` 的轮询逻辑，兼容 Tokio 异步运行时的驱动机制。

---

#### 在项目中的角色