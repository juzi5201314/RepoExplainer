# `reap.rs` 文件详解

## 文件目的
该文件实现了 Tokio 进程管理模块中用于监控子进程退出状态的核心组件 `Reaper`。它通过异步信号处理和轮询机制，协调子进程退出状态的获取，并确保僵尸进程（zombie）被正确回收。

---

## 关键组件

### 1. **`Reaper` 结构体**
```rust
pub(crate) struct Reaper<W, Q, S>
where
    W: Wait,
    Q: OrphanQueue<W>,
{
    inner: Option<W>,
    orphan_queue: Q,
    signal: S,
}
```
- **职责**：协调子进程退出状态的监控与回收。
- **字段**：
  - `inner`: 存储实际的子进程句柄（如 `StdChild`）。
  - `orphan_queue`: 管理孤儿进程的队列（实现 `OrphanQueue` trait）。
  - `signal`: 监听 `SIGCHLD` 信号的流（实现 `InternalStream` trait）。

---

### 2. **`Future` 实现**
```rust
impl<W, Q, S> Future for Reaper<W, Q, S> { ... }
```
- **输出类型**：`io::Result<ExitStatus>`，返回子进程的退出状态。
- **核心逻辑**：
  - **信号注册**：通过 `signal.poll_recv` 注册对 `SIGCHLD` 信号的兴趣，确保任务在信号到达时被唤醒。
  - **轮询退出状态**：调用 `inner.try_wait()` 检查子进程是否已退出。
  - **循环机制**：若未退出且信号未到达，则持续轮询，直到获取退出状态或进入等待状态（`Poll::Pending`）。

---

### 3. **`Kill` 特性实现**
```rust
impl<W, Q, S> Kill for Reaper<W, Q, S> { ... }
```
- **功能**：通过 `kill()` 方法向子进程发送终止信号。
- **实现**：委托给内部 `inner` 的 `Kill` 实现。

---

### 4. **`Drop` 实现**
```rust
impl<W, Q, S> Drop for Reaper<W, Q, S> { ... }
```
- **作用**：在 `Reaper` 被丢弃时处理未退出的子进程：
  - 若子进程已退出，则直接返回。
  - 否则将子进程加入孤儿队列，避免成为僵尸进程。

---

## 关键机制

### 信号与轮询的协调
- **信号驱动**：通过 `SIGCHLD` 信号通知子进程退出事件，避免持续轮询浪费资源。
- **防死锁设计**：在调用 `try_wait` 前预先注册信号监听，确保即使信号在两次轮询间到达也能被正确处理。

### 孤儿进程管理
- **孤儿队列**：当 `Reaper` 被丢弃但子进程未退出时，将子进程加入 `orphan_queue`，由全局队列后续处理。

---

## 在项目中的角色
该文件是 Tokio 进程管理模块的核心组件，负责异步监控子进程退出状态、处理信号事件，并确保资源正确回收，是 Tokio 实现异步进程管理的关键实现。
