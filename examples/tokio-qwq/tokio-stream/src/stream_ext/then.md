# `then.rs` 文件详解

## 文件目的
该文件实现了 Tokio 流（Stream）扩展中的 `then` 方法，用于对流中的每个元素执行异步转换操作。通过将闭包返回的 `Future` 与流的元素结合，实现异步处理流程的无缝衔接。

---

## 核心组件

### 1. `Then` 结构体
```rust
pub struct Then<St, Fut, F> {
    #[pin] stream: St,
    #[pin] future: Option<Fut>,
    f: F,
}
```
- **字段说明**：
  - `stream`: 原始流，使用 `#[pin]` 标记以支持 `Pin` 语法，确保内存不被移动。
  - `future`: 当前正在处理的异步任务（`Future`），初始为 `None`。
  - `f`: 用户提供的闭包，将流元素转换为 `Future`。

- **功能**：
  - 封装流和异步处理逻辑，管理中间状态（如未完成的 `Future`）。

---

### 2. `impl Stream` 特征实现
```rust
impl<St, Fut, F> Stream for Then<St, Fut, F> 
where 
    St: Stream, 
    Fut: Future, 
    F: FnMut(St::Item) -> Fut 
{
    type Item = Fut::Output;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Fut::Output>> {
        // 核心逻辑
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        // 调整大小提示
    }
}
```

#### 关键方法：
- **`poll_next`**：
  - **流程**：
    1. 检查是否有未完成的 `Future`（`future` 字段）：
       - 若存在，先尝试完成该 `Future`，返回结果。
       - 若未完成，暂停轮询。
    2. 若无未完成的 `Future`，从流中获取下一个元素：
       - 将元素传递给闭包 `f`，生成新 `Future` 并存入 `future`。
       - 循环重复上述步骤。
  - **作用**：协调流元素与异步任务的执行顺序，确保每个元素的异步处理完成后才继续处理下一个元素。

- **`size_hint`**：
  - 根据当前流和未完成的 `Future` 数量调整大小提示，提供更准确的流长度估计。

---

### 3. 辅助实现
- **`Debug` 特征**：
  ```rust
  impl<St, Fut, F> fmt::Debug for Then<St, Fut, F> 
  where 
      St: fmt::Debug 
  {
      fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { ... }
  }
  ```
  - 允许通过 `Debug` 格式化输出流的内部状态。

- **`new` 构造函数**：
  ```rust
  pub(super) fn new(stream: St, f: F) -> Self { ... }
  ```
  - 初始化 `Then` 实例，初始无未完成的 `Future`。

---

## 在项目中的作用
该文件为 Tokio 流框架提供了 `then` 方法的核心实现，允许开发者对流中的每个元素执行异步转换操作。通过将闭包返回的 `Future` 与流的轮询机制结合，实现了异步流处理的灵活性和高效性，是 Tokio 异步编程模型的重要组成部分。
