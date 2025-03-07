### 文件说明：`poll_semaphore.rs`

#### **目的**
该文件实现了 `PollSemaphore` 结构体，这是一个对 Tokio 标准库中 `Semaphore` 的封装。其核心目标是提供一个支持轮询（poll-based）的信号量接口，允许在异步任务中高效获取许可，同时避免频繁的内存分配。

---

#### **关键组件**

1. **结构体定义**
   ```rust
   pub struct PollSemaphore {
       semaphore: Arc<Semaphore>,
       permit_fut: Option<(u32, ReusableBoxFuture<'static, Result<OwnedSemaphorePermit, AcquireError>>)>,
   }
   ```
   - **`semaphore`**: 内部持有的 Tokio 原始信号量，通过 `Arc` 实现共享。
   - **`permit_fut`**: 存储当前正在轮询的许可获取 Future，包含请求的许可数量和复用的 Future 对象。

2. **核心方法**
   - **`poll_acquire` 和 `poll_acquire_many`**  
     这两个方法是核心接口，用于尝试获取许可：
     - 当许可可用时，直接返回 `Poll::Ready(Some(permit))`。
     - 当无许可时，返回 `Poll::Pending` 并注册任务唤醒。
     - 通过 `ReusableBoxFuture` 复用 Future 对象，减少内存分配开销。
     - 支持指定获取多个许可（`poll_acquire_many`）。

   - **`available_permits` 和 `add_permits`**  
     直接转发到内部 `Semaphore`，提供获取可用许可数和增加许可数的功能。

3. **Trait 实现**
   - **`Stream` Trait**: 使 `PollSemaphore` 可以作为流（Stream）使用，通过 `poll_next` 方法获取许可。
   - **`Clone` Trait**: 允许创建共享同一内部信号量的新实例。
   - **`Debug` 和 `AsRef<Semaphore>`**: 提供调试信息和类型转换支持。

---

#### **实现细节**
- **Future 复用优化**  
  使用 `ReusableBoxFuture` 存储 Future 对象，避免每次调用时重新分配内存。当请求的许可数变化时，会更新 Future 的参数但复用其结构，显著提升性能。
  
- **任务唤醒机制**  
  在 `Poll::Pending` 状态时，通过 `Context` 注册当前任务的 `Waker`，当信号量状态变化时（许可可用或关闭），会唤醒等待的任务。

- **错误处理**  
  若信号量已关闭（`Closed`），返回 `Poll::Ready(None)`；若成功获取许可则返回 `Some(permit)`。

---

#### **项目中的角色**