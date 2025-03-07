# 代码文件解释：`timeout.rs`

## 目的
该文件实现了 Tokio 流（Stream）的超时功能。通过包装原始流，当流在指定时间内未产生新项时，返回超时错误（`Elapsed`）。这是异步编程中处理流阻塞或延迟的重要工具。

---

## 核心组件

### 1. **`Timeout<S>` 结构体**
```rust
pub struct Timeout<S> {
    #[pin] stream: Fuse<S>,
    #[pin] deadline: Sleep,
    duration: Duration,
    poll_deadline: bool,
}
```
- **功能**：包装原始流并添加超时逻辑。
- **字段**：
  - `Fuse<S>`：确保流在完成时自动终止，避免重复轮询。
  - `Sleep`：定时器，用于跟踪超时时间。
  - `duration`：超时时间间隔。
  - `poll_deadline`：标记是否需要检查定时器。

---

### 2. **错误类型 `Elapsed`**
```rust
pub struct Elapsed(());
```
- **功能**：表示超时错误。
- **实现**：
  - 实现 `Display` 和 `Error` trait，支持错误信息输出。
  - 可转换为 `std::io::Error`，便于与标准库集成。

---

### 3. **`Timeout` 的 `Stream` trait 实现**
```rust
impl<S: Stream> Stream for Timeout<S> {
    type Item = Result<S::Item, Elapsed>;

    fn poll_next(...) {
        // 核心逻辑
    }
}
```
- **`poll_next` 方法流程**：
  1. **检查原始流**：若流有新项，更新超时时间并返回 `Ok(item)`。
  2. **流未就绪时检查超时**：
     - 若定时器到期且 `poll_deadline` 为 `true`，返回 `Err(Elapsed)`。
     - 否则标记 `poll_deadline` 为 `false`，等待下次轮询。
  3. **超时重置**：每次流产生新项后，重新设置超时时间。

---

### 4. **`size_hint` 调整**
```rust
fn size_hint(&self) -> (usize, Option<usize>) {
    // 上界计算为原始流的两倍加一
    (lower, twice_plus_one(upper))
}
```
- **原因**：超时可能在每项之间插入错误，因此上界需扩展为 `2×原始上界 + 1`。

---

## 工作原理
1. **初始化**：通过 `Timeout::new` 设置超时时间，启动定时器。
2. **轮询流**：每次轮询时先检查原始流是否有新项。
3. **超时检查**：若流未就绪且定时器到期，则触发超时错误。
4. **重置机制**：流产生新项后，重新启动定时器。

---

## 项目中的角色