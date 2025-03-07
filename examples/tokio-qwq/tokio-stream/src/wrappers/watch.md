### 文件说明

#### 目的
该文件实现了 `tokio::sync::watch::Receiver` 的流（Stream）适配器 `WatchStream`，允许通过 `Stream` trait 的 `next()` 方法异步消费观察者通道（watch channel）中的值。通过两种不同的构造方式控制初始值的返回行为。

#### 关键组件

1. **结构体定义**
   ```rust
   pub struct WatchStream<T> {
       inner: ReusableBoxFuture<'static, (Result<(), RecvError>, Receiver<T>)>,
   }
   ```
   - 使用 `ReusableBoxFuture` 存储异步任务，复用 future 避免重复分配
   - 存储 `Receiver<T>` 实现通道值的监听

2. **构造方法**
   ```rust
   pub fn new(rx: Receiver<T>) -> Self { ... }
   pub fn from_changes(rx: Receiver<T>) -> Self { ... }
   ```
   - `new()`：立即返回通道当前值（包括初始值）
   - `from_changes()`：仅在值变化时触发（跳过初始值）

3. **Stream 实现**
   ```rust
   impl<T: Clone + Send + Sync> Stream for WatchStream<T> {
       fn poll_next(...) -> Poll<Option<T>> { ... }
   }
   ```
   - 核心逻辑：通过 `poll()` 驱动 future 监听通道变化
   - 成功时克隆当前值并重置 future
   - 失败时返回 `None` 并继续监听（可能因发送端关闭）

4. **辅助函数**
   ```rust
   async fn make_future<T>(rx: Receiver<T>) -> (Result<(), RecvError>, Receiver<T>) { ... }
   ```
   封装 `Receiver.changed()` 的异步等待逻辑

#### 行为特点
- **初始值处理**：
  - `new()` 立即返回初始值（如示例中首次 `next()` 得到 "hello"）
  - `from_changes()` 忽略初始值（需等待 `send()` 后触发）
- **值获取**：
  使用 `borrow_and_update()` 安全获取当前值，无需消耗所有权
- **错误处理**：
  发送端关闭时返回 `RecvError`，流结束返回 `Poll::Ready(None)`

#### 在项目中的角色