# `tokio/src/runtime/local_runtime/runtime.rs` 文件详解

## 文件目的
此文件实现了 Tokio 的 `LocalRuntime` 运行时，专为支持非 `Send + Sync` 的本地任务而设计。它允许直接使用 `spawn_local` 方法而无需 `LocalSet` 上下文，并且只能在创建线程上运行，无法跨线程移动或驱动。

---

## 核心组件与功能

### 1. **`LocalRuntime` 结构体**
```rust
pub struct LocalRuntime {
    scheduler: LocalRuntimeScheduler,
    handle: Handle,
    blocking_pool: BlockingPool,
    _phantom: PhantomData<*mut u8>,
}
```
- **`scheduler`**: 当前仅支持 `CurrentThread` 调度器，负责任务调度。
- **`handle`**: 运行时句柄，提供任务调度和资源管理接口。
- **`blocking_pool`**: 管理阻塞任务的线程池。
- **`_phantom`**: 通过 `!Send + !Sync` 标记确保运行时不能跨线程传递。

---

### 2. **关键方法**
#### a. **`new()`**
```rust
pub fn new() -> std::io::Result<LocalRuntime> {
    Builder::new_current_thread()
        .enable_all()
        .build_local(&Default::default())
}
```
- 使用 `Builder` 配置并创建默认的单线程本地运行时，启用所有 I/O 和时钟驱动。

#### b. **`spawn_local()`**
```rust
pub fn spawn_local<F>(&self, future: F) -> JoinHandle<F::Output>
where
    F: Future + 'static,
    F::Output: 'static,
{
    // 根据 Future 大小选择堆栈或堆分配
    if mem::size_of::<F>() > BOX_FUTURE_THRESHOLD {
        self.handle.spawn_local_named(Box::pin(future), meta)
    } else {
        self.handle.spawn_local_named(future, meta)
    }
}
```
- 允许直接提交非 `Send` 的异步任务，自动处理栈上或堆上的 Future。

#### c. **`block_on()`**
```rust
pub fn block_on<F: Future>(&self, future: F) -> F::Output {
    // 内部调用 block_on_inner 执行 Future
    if std::mem::size_of::<F>() > BOX_FUTURE_THRESHOLD {
        self.block_on_inner(Box::pin(future), meta)
    } else {
        self.block_on_inner(future, meta)
    }
}
```
- 阻塞当前线程直至 Future 完成，是运行时的入口方法。

#### d. **`enter()`**
```rust
pub fn enter(&self) -> EnterGuard<'_> {
    self.handle.enter()
}
```
- 提供运行时上下文，允许在当前线程创建需要执行环境的类型（如 `Sleep` 或 `TcpStream`）。

#### e. **`shutdown_timeout()` 和 `shutdown_background()`**
```rust
pub fn shutdown_timeout(mut self, duration: Duration) {
    self.handle.inner.shutdown();
    self.blocking_pool.shutdown(Some(duration));
}

pub fn shutdown_background(self) {
    self.shutdown_timeout(Duration::from_nanos(0));
}
```
- 安全终止运行时，可等待指定时间或立即释放资源（可能遗留阻塞任务）。

---

### 3. **生命周期管理**
- **`Drop` 实现**：
  ```rust
  impl Drop for LocalRuntime {
      fn drop(&mut self) {
          if let LocalRuntimeScheduler::CurrentThread(current_thread) = &mut self.scheduler {
              current_thread.shutdown(&self.handle.inner);
          }
      }
  }
  ```
  - 确保在销毁时正确关闭调度器和任务，避免资源泄漏。

---

## 与其他组件的协作
- **`BlockingPool`**: 管理阻塞任务的线程池，与 `spawn_blocking` 方法配合。
- **`Handle`**: 提供跨线程任务调度能力，但仅支持 `Send` 任务。
- **`CurrentThread` 调度器**: 实现单线程任务调度逻辑，确保本地任务在当前线程执行。

---

## 在项目中的角色