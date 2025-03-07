# 文件说明：`tokio/src/task/yield_now.rs`

## 文件目的
该文件实现了 Tokio 运行时的 `yield_now` 功能，允许当前任务主动让出执行权，将控制权交还给运行时，以便其他任务有机会运行。这是 Tokio 协作式调度的核心机制之一。

---

## 关键组件与实现细节

### 1. `yield_now` 函数
```rust
pub async fn yield_now() { ... }
```
- **功能**：通过 `await` 语法让当前任务暂停执行，返回运行时调度器。
- **实现方式**：通过内部定义的 `YieldNow` 结构体实现 `Future` trait，利用异步语法糖展开为状态机。

### 2. `YieldNow` 结构体
```rust
struct YieldNow {
    yielded: bool,
}
```
- **字段**：
  - `yielded`: 布尔标志，标记是否已执行过让出操作（初始为 `false`）。

### 3. `Future` 实现
```rust
impl Future for YieldNow {
    fn poll(&mut self, cx: &mut Context<'_>) -> Poll<()> {
        if self.yielded {
            return Poll::Ready(());
        }
        self.yielded = true;
        context::defer(cx.waker());
        Poll::Pending
    }
}
```
- **首次调用流程**：
  1. 设置 `yielded` 为 `true`。
  2. 调用 `context::defer(cx.waker())`：将当前任务的 `Waker` 延迟注册到运行时的调度队列末尾。
  3. 返回 `Poll::Pending`，表明任务暂停。
- **后续调用**：当再次被调度时，直接返回 `Poll::Ready(())` 完成 Future。

---

## 运行时集成与行为特点

### 1. 调度机制
- **队列行为**：任务让出后会被放置到调度队列的**末尾**，确保其他等待任务优先执行。
- **非保证特性**：
  - 若调用栈中存在 `tokio::select!` 等特殊组合器，可能无法完全返回运行时。
  - 运行时可能立即重新调度当前任务，不保证其他任务会被优先执行（如未触发 I/O 事件时）。

### 2. 性能与限制
- **无锁设计**：通过非阻塞的 `defer` 机制实现协作式调度。
- **适用场景**：在密集循环或高优先级任务中主动让步，避免饿死其他任务。

---

## 文件在项目中的角色
该文件为 Tokio 运行时提供了核心的 `yield_now` 功能，通过协作式让步机制实现任务调度的公平性，是 Tokio 异步任务管理系统的重要组成部分。
