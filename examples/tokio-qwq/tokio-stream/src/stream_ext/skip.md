# `tokio-stream/src/stream_ext/skip.rs` 文件详解

## **文件目的**
该文件实现了 Tokio 异步流（`Stream`）的 `skip` 扩展方法，用于跳过流中的前 `n` 个元素。通过封装原始流并跟踪剩余需跳过的元素数量，提供符合异步流语义的跳过逻辑。

---

## **核心组件**

### **1. `Skip` 结构体**
```rust
pin_project! {
    pub struct Skip<St> {
        #[pin]
        stream: St,
        remaining: usize,
    }
}
```
- **功能**：包装原始流并记录剩余需跳过的元素数量。
- **字段**：
  - `stream`: 被封装的原始流，使用 `#[pin]` 标记以支持 `Pin` 语义。
  - `remaining`: 需跳过的剩余元素计数器。

### **2. 调试支持**
```rust
impl<St: fmt::Debug> fmt::Debug for Skip<St> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Skip")
            .field("stream", &self.stream)
            .finish()
    }
}
```
- 提供 `Debug` 格式化输出，展示内部流和剩余计数。

### **3. 构造方法**
```rust
pub(super) fn new(stream: St, remaining: usize) -> Self {
    Self { stream, remaining }
}
```
- 初始化 `Skip` 实例，传入原始流和需跳过的元素数量。

---

## **Stream Trait 实现**

### **1. `poll_next` 方法**
```rust
fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
    loop {
        match ready!(self.as_mut().project().stream.poll_next(cx)) {
            Some(e) => {
                if self.remaining == 0 {
                    return Poll::Ready(Some(e));
                }
                *self.as_mut().project().remaining -= 1;
            }
            None => return Poll::Ready(None),
        }
    }
}
```
- **逻辑**：
  1. 循环轮询底层流的 `poll_next`。
  2. 若剩余计数 `remaining` 为 0，返回当前元素。
  3. 否则，递减计数器并继续跳过元素。
  4. 流结束时返回 `None`。
- **关键点**：使用 `ready!` 宏处理异步等待，确保仅在元素就绪时继续处理。

### **2. `size_hint` 方法**
```rust
fn size_hint(&self) -> (usize, Option<usize>) {
    let (lower, upper) = self.stream.size_hint();
    let lower = lower.saturating_sub(self.remaining);
    let upper = upper.map(|x| x.saturating_sub(self.remaining));
    (lower, upper)
}
```
- 调整原始流的 `size_hint`，减去需跳过的元素数量，避免负值。

---

## **项目中的角色**
该文件为 Tokio 异步流提供 `skip` 扩展能力，允许开发者跳过流的前 `n` 个元素，是 Tokio 流处理功能的重要组成部分，支持构建更复杂的异步数据处理管道。

```rust
// 使用示例：
// let skipped_stream = my_stream.skip(5);
```

## **在项目中的定位**
此文件属于 Tokio 流扩展库（`tokio-stream`）的核心实现之一，通过组合原始流并修改其行为，为异步流处理提供标准操作（如 `skip`），是构建异步数据处理流水线的基础组件。
```
