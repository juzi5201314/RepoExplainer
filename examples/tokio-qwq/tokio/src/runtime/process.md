# 文件解释：`tokio/src/runtime/process.rs`

## **文件目的**  
该文件实现了 Tokio 运行时的进程驱动（Process Driver），主要负责在 Unix 平台上清理因父进程提前退出而成为“孤儿”的子进程。通过集成信号处理机制，确保在异步任务等待期间主动回收这些孤儿进程，避免资源泄漏。

---

## **关键组件与功能**

### **1. `Driver` 结构体**
```rust
pub(crate) struct Driver {
    park: SignalDriver,
    signal_handle: SignalHandle,
}
```
- **职责**：管理进程的生命周期，特别是在异步任务等待时触发孤儿进程的回收。
- **字段**：
  - `park`: 信号驱动实例，用于协调异步任务的阻塞与唤醒。
  - `signal_handle`: 信号句柄，用于监听和处理子进程终止信号（如 `SIGCHLD`）。

---

### **2. 核心方法**

#### **`new` 方法**
```rust
pub(crate) fn new(park: SignalDriver) -> Self {
    let signal_handle = park.handle();
    Self { park, signal_handle }
}
```
- **功能**：初始化 `Driver` 实例，绑定信号驱动和句柄，确保后续操作能通过信号处理机制触发进程回收。

---

#### **`park` 和 `park_timeout` 方法**
```rust
pub(crate) fn park(&mut self, handle: &driver::Handle) {
    self.park.park(handle);
    GlobalOrphanQueue::reap_orphans(&self.signal_handle);
}

pub(crate) fn park_timeout(&mut self, handle: &driver::Handle, duration: Duration) {
    self.park.park_timeout(handle, duration);
    GlobalOrphanQueue::reap_orphans(&self.signal_handle);
}
```
- **功能**：
  - `park`: 阻塞当前线程，等待异步任务的唤醒。
  - `park_timeout`: 在指定超时时间后唤醒。
- **关键操作**：在每次阻塞或超时后，调用 `GlobalOrphanQueue::reap_orphans` 回收已终止的孤儿进程。  
- **原理**：通过信号机制捕获子进程终止事件，确保 Tokio 运行时及时清理资源。

---

#### **`shutdown` 方法**
```rust
pub(crate) fn shutdown(&mut self, handle: &driver::Handle) {
    self.park.shutdown(handle);
}
```
- **功能**：关闭信号驱动，释放相关资源，结束进程驱动的生命周期。

---

## **与其他模块的协作**
- **`GlobalOrphanQueue`**: 存储并管理需要回收的孤儿进程，`reap_orphans` 方法会遍历并清理这些进程。
- **`SignalDriver` 和 `SignalHandle`**: 提供信号监听和处理能力，捕获子进程终止信号（如 `SIGCHLD`），触发回收逻辑。

---

## **在项目中的角色**
该文件是 Tokio 运行时进程管理的核心组件，通过信号驱动和主动回收机制，确保异步任务在等待期间不会因孤儿进程泄漏资源，保障运行时的稳定性和资源高效利用。

最后描述：  