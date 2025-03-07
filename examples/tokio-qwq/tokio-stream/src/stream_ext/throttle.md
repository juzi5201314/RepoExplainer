# 代码文件解释：`throttle.rs`

## **功能与目的**
该文件实现了 Tokio 流（Stream）的 `throttle` 扩展，用于**在流的相邻元素之间强制执行固定延迟**。其核心作用是通过引入时间间隔来控制流的处理速度，适用于需要速率限制的场景（如 API 请求限流、事件处理等）。

---

## **关键组件与实现细节**

### **1. `Throttle` 结构体**
```rust
pub struct Throttle<T> {
    #[pin] delay: Sleep,
    duration: Duration,
    has_delayed: bool,
    #[pin] stream: T,
}
```
- **字段说明**：
  - `delay`: 使用 `tokio::time::Sleep` 实现延迟逻辑。
  - `duration`: 用户指定的相邻元素之间的最小时间间隔。
  - `has_delayed`: 标记当前是否已触发延迟（但流尚未返回新元素）。
  - `stream`: 需要被限流的原始流。

- **特性**：
  - 通过 `pin_project_lite` 宏实现 `Unpin` 的兼容性，需通过 `Box::pin` 显式固定内存位置。
  - 提供 `get_ref`、`get_mut` 和 `into_inner` 方法，允许访问或释放底层流。

---

### **2. 核心逻辑：`poll_next` 方法**
```rust
fn poll_next(self: Pin<&mut Self>, cx: &mut task::Context<'_>) -> Poll<Option<Self::Item>> {
    // ...
}
```
- **流程解析**：
  1. **检查延迟状态**：
     - 如果 `has_delayed` 为 `false` 且延迟时间不为零，则等待 `delay` 完成。
     - 延迟完成后将 `has_delayed` 设为 `true`。
  2. **获取流的下一个元素**：
     - 调用 `stream.poll_next` 获取元素。
     - 若成功获取元素（`value.is_some()`），则：
       - 重置 `delay` 为当前时间 + `duration`，准备下一次延迟。
       - 将 `has_delayed` 设为 `false`，确保下次获取元素前必须等待延迟。
  3. **返回结果**：将流返回的元素包装为 `Poll::Ready`。

- **关键逻辑**：
  - **延迟重置机制**：每次成功获取元素后，立即重置延迟计时器，确保相邻元素之间始终间隔 `duration`。
  - **零延迟处理**：若 `duration` 为零，则直接返回流元素，不执行延迟。

---

### **3. 辅助函数**
- **`throttle` 函数**：
  ```rust
  pub(super) fn throttle<T>(duration: Duration, stream: T) -> Throttle<T> { /* ... */ }
  ```
  - 初始化 `Throttle` 结构体，设置初始延迟为 `duration` 后的时间点。

- **`is_zero` 函数**：
  ```rust
  fn is_zero(dur: Duration) -> bool { dur == Duration::from_millis(0) }
  ```
  - 判断延迟时间是否为零，用于跳过无效延迟。

---

## **项目中的角色**