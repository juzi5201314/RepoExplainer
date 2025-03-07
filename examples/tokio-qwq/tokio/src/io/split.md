### 文件说明

#### 目的
该文件实现了将同时支持异步读写（`AsyncRead + AsyncWrite`）的流对象拆分为独立的只读（`ReadHalf`）和只写（`WriteHalf`）句柄的功能。通过拆分，可以将读写操作分离到不同任务中，提升并发性能，同时保证线程安全。

#### 核心组件
1. **`ReadHalf<T>` 和 `WriteHalf<T>` 结构体**
   - 通过 `Arc<Inner<T>>` 共享底层资源：
     - `Inner<T>` 包含 `Mutex<T>` 保护的原始流对象，确保多线程安全访问。
     - `is_write_vectored` 标记是否支持向量写操作。
   - 实现 `AsyncRead` 和 `AsyncWrite` trait：
     - `ReadHalf` 通过 `poll_read` 方法实现异步读取。
     - `WriteHalf` 通过 `poll_write`、`poll_flush` 等方法实现异步写入及流控制。

2. **`split` 函数**
   - 输入：支持 `AsyncRead + AsyncWrite` 的流对象。
   - 输出：拆分后的 `ReadHalf` 和 `WriteHalf`。
   - 实现：通过 `Arc` 和 `Mutex` 将流对象包装为共享状态，确保两个句柄安全访问。

3. **合并功能**
   - `unsplit` 方法：将拆分后的两个句柄重新合并为原始流对象。
   - 安全性：通过 `Arc::ptr_eq` 检查是否为同一对，否则触发 panic。

4. **线程安全与同步**
   - 使用 `Arc` 实现跨线程共享。
   - `Mutex` 确保对流对象的互斥访问。
   - `unsafe impl Send/Sync` 标记，明确结构体的线程安全性。

#### 工作原理
1. **拆分过程**
   - 调用 `split(stream)` 时，原始流被包装到 `Inner<T>` 的 `Mutex` 中。
   - 通过 `Arc` 克隆出两个句柄，共享同一 `Inner` 实例。

2. **操作隔离**
   - 读写操作通过 `Inner::with_lock` 获取锁，确保同一时间只有一个操作访问流对象。
   - 例如，`ReadHalf` 的 `poll_read` 直接调用原始流的 `poll_read`，但通过锁保证线程安全。

3. **合并机制**
   - `unsplit` 验证两个句柄的 `Arc` 指向同一 `Inner`，若通过则释放锁并返回原始流。

#### 项目中的角色