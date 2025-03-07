# 文件解释：`timeout_repeating.rs`

## 文件目的
该文件实现了 Tokio 流扩展中的 `timeout_repeating` 特性，为流添加可重复触发的超时机制。当流在指定时间间隔内未产生新项时，会持续返回超时错误，直到流恢复或关闭。

---

## 核心组件

### 1. `TimeoutRepeating` 结构体
```rust
pin_project! {
    pub struct TimeoutRepeating<S> {
        #[pin] stream: Fuse<S>,
        #[pin] interval: Interval,
    }
}
```
- **`Fuse<S>`**：包裹原始流的熔断包装器，记录流是否已结束。
- **`Interval`**：Tokio 定时器，用于周期性检查流的活跃性。
- **功能**：通过组合流和定时器，实现超时逻辑。

---

### 2. 核心方法

#### `new` 构造函数
```rust
pub(super) fn new(stream: S, interval: Interval) -> Self { ... }
```
- 初始化 `TimeoutRepeating`，将原始流包装为熔断流，并绑定定时器。

#### `poll_next` 方法
```rust
fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Result<S::Item, Elapsed>>> {
    // ...
}
```
- **流程**：
  1. 首先尝试从熔断流获取新项：
     - 若成功获取项，重置定时器 (`interval.reset()`)。
     - 若流已结束 (`v.is_some()` 为 false)，直接返回结果。
  2. 若流未就绪 (`Poll::Pending`)，则轮询定时器：
     - 定时器触发时，返回 `Err(Elapsed)` 表示超时。
- **关键逻辑**：通过重置定时器实现超时时间的动态刷新，确保每次流产生新项时重新开始计时。

#### `size_hint` 方法
```rust
fn size_hint(&self) -> (usize, Option<usize>) { ... }
```
- 返回 `(lower, None)` 表示流可能无限期产生超时错误，直到原始流关闭。

---

## 工作原理
1. **正常流处理**：当原始流正常产生项时，每次新项触发会重置定时器，避免超时。
2. **超时触发**：若流在 `Interval` 时间内未产生新项，定时器触发时返回 `Elapsed` 错误。
3. **持续错误**：流结束后或长时间无响应时，每次轮询都会触发定时器并返回错误。

---

## 项目中的角色
该文件为 Tokio 流提供可重复超时功能，用于监控流的活跃性，确保在预期时间内检测到流的不活跃状态，常用于需要持续活动验证的场景（如网络连接保活、任务心跳检测）。  