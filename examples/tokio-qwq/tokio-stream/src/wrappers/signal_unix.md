### 文件说明

#### 目的
该文件实现了 `SignalStream` 结构体，将 Tokio 的 `Signal` 类型适配为符合 `Stream` trait 的异步流。其核心目的是让 Unix 系统的信号事件能够通过流式接口（如 `StreamExt`）进行异步处理，例如通过 `next()` 方法逐个消费信号。

#### 关键组件
1. **结构体定义**
   ```rust
   pub struct SignalStream {
       inner: Signal,
   }
   ```
   - 包裹 `tokio::signal::unix::Signal` 实例，提供对信号的封装。

2. **构造方法**
   ```rust
   pub fn new(signal: Signal) -> Self { ... }
   ```
   - 创建 `SignalStream` 实例，直接接收 `Signal` 对象。

3. **转换方法**
   ```rust
   pub fn into_inner(self) -> Signal { ... }
   ```
   - 将 `SignalStream` 转换回原始 `Signal` 对象，便于直接操作底层信号句柄。

4. **Stream Trait 实现**
   ```rust
   impl Stream for SignalStream {
       type Item = ();
       fn poll_next(...) -> Poll<Option<()>> { ... }
   }
   ```
   - 通过 `poll_next` 方法将 `Signal` 的 `poll_recv` 轮询逻辑映射到流接口，返回 `()` 表示信号触发。

5. **AsRef/AsMut 实现**
   ```rust
   impl AsRef<Signal> for SignalStream { ... }
   impl AsMut<Signal> for SignalStream { ... }
   ```
   - 提供对内部 `Signal` 的不可变/可变引用访问，支持直接调用底层方法（如设置信号类型）。

#### 工作原理
- **信号监听**：通过 `tokio::signal::unix::signal` 创建 `Signal` 对象，指定监听的信号类型（如 `SIGTERM`）。
- **流式转换**：将 `Signal` 封装为 `SignalStream`，使其支持 `Stream` trait 的异步轮询。
- **事件消费**：通过 `StreamExt` 的 `next()` 方法异步等待信号触发，每次触发时流返回 `Some(())`，流不会终止。

#### 项目中的角色
该文件是 Tokio Stream 库的 Unix 平台专用适配器，将底层信号处理接口与流式异步编程模型结合，使开发者能够以统一的方式处理异步事件（如信号、网络请求等），是构建异步信号监听功能的核心组件。
