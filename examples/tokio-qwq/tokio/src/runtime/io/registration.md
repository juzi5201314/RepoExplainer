### 文件说明：`tokio/src/runtime/io/registration.rs`

#### **文件目的**
该文件定义了 Tokio 运行时中用于管理 I/O 资源与事件循环（reactor）关联的核心结构 `Registration`。它的主要职责是：
1. 将 I/O 资源注册到事件循环中，以便在资源就绪时触发任务通知。
2. 提供对读写就绪状态的轮询接口，支持异步 I/O 操作。
3. 确保 I/O 资源的生命周期与事件循环正确绑定，并在资源释放时解除注册。

---

#### **关键组件**

##### **结构体 `Registration`**
```rust
pub(crate) struct Registration {
    handle: scheduler::Handle,
    shared: Arc<ScheduledIo>,
}
```
- **`handle`**：指向运行时调度器的句柄，用于与事件循环交互。
- **`shared`**：共享的 `ScheduledIo` 状态，存储 I/O 资源的就绪事件和调度信息。

##### **核心方法**
1. **`new_with_interest_and_handle`**
   - **功能**：将 I/O 资源（如套接字、文件描述符）注册到事件循环。
   - **参数**：
     - `io`: 需要注册的 I/O 资源（实现 `mio::Source`）。
     - `interest`: 关注的就绪事件类型（如可读、可写）。
     - `handle`: 运行时调度器的句柄。
   - **返回**：成功注册后返回 `Registration` 实例。

2. **`deregister`**
   - **功能**：从事件循环中注销 I/O 资源，释放相关资源。
   - **注意**：必须在 I/O 资源被丢弃前调用，否则可能导致资源泄漏。

3. **`poll_read_ready` 和 `poll_write_ready`**
   - **功能**：轮询 I/O 资源的读/写就绪状态。
   - **实现**：
     - 使用 `poll_ready` 内部方法检查就绪事件。
     - 通过 `Context` 参数关联异步任务，当资源就绪时唤醒任务。

4. **`poll_io` 和 `try_io`**
   - **`poll_io`**：执行实际的 I/O 操作（如读写），若阻塞则等待资源就绪。
   - **`try_io`**：非阻塞尝试执行 I/O 操作，若未就绪则返回 `WouldBlock`。

5. **`async_io` 和 `readiness`**
   - **`async_io`**：异步等待资源就绪后执行 I/O 操作。
   - **`readiness`**：异步等待指定的就绪事件发生。

---

#### **关键行为**
1. **就绪事件管理**
   - 通过 `ScheduledIo` 跟踪 I/O 资源的就绪状态。
   - 使用 `mio` 库与操作系统事件循环（如 epoll/kqueue）交互。
   - 当事件循环检测到资源就绪时，会更新 `ScheduledIo` 的状态并通知等待的任务。

2. **任务通知机制**
   - `poll_read_ready` 和 `poll_write_ready` 方法通过 `Context` 将任务挂起，直到资源就绪。
   - 采用 `Poll` 枚举返回结果，支持异步操作的挂起和恢复。

3. **线程安全与限制**
   - `Registration` 实现了 `Send` 和 `Sync`，但要求：
     - 同一时间最多只能有一个任务调用 `poll_read_ready`。
     - 同一时间最多只能有一个任务调用 `poll_write_ready`。
   - 违反此限制可能导致通知丢失或任务阻塞。

---

#### **在项目中的角色**
该文件是 Tokio 运行时 I/O 子系统的底层核心组件，负责将用户态的 I/O 操作与操作系统事件循环绑定，提供异步就绪通知和资源管理功能，是实现 Tokio 异步 I/O 的关键基础设施。
