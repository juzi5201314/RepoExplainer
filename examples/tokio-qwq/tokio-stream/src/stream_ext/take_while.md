# 文件解释：`take_while.rs`

## 目的
该文件实现了 Tokio 流（Stream）的 `take_while` 扩展方法，提供了一个按条件终止流处理的适配器。当流中的元素不再满足指定谓词时，该适配器会停止进一步的处理。

---

## 核心组件

### 1. `TakeWhile` 结构体
```rust
pub struct TakeWhile<St, F> {
    #[pin] stream: St,
    predicate: F,
    done: bool,
}
```
- **`stream`**：被包装的原始流，使用 `#[pin]` 标记以支持 Pin 语义。
- **`predicate`**：用户提供的谓词函数，类型为 `FnMut(&Item) -> bool`。
- **`done`**：布尔标志，标记是否已停止处理。

#### 特性实现
- **`Debug`**：通过 `fmt::Debug` 显示内部流和 `done` 状态。
- **`new` 构造函数**：初始化结构体，初始 `done` 为 `false`。

---

### 2. `Stream` 特性实现
```rust
impl<St, F> Stream for TakeWhile<St, F> { ... }
```
#### 核心方法
- **`poll_next`**：
  1. 当 `done` 为 `false` 时，调用底层流的 `poll_next` 获取元素。
  2. 对返回的元素应用谓词：
     - 若谓词返回 `false`，设置 `done = true` 并停止后续处理。
     - 若返回 `true`，则返回该元素。
  3. 若 `done` 已为 `true`，直接返回 `None`。
- **`size_hint`**：
  - 当未完成时，下界设为 `0`（因无法预知满足条件的元素数量），上界继承原始流的上界。

---

### 3. 关键逻辑分析
- **条件终止**：通过 `predicate` 函数动态判断是否继续处理元素。
- **状态管理**：`done` 标志确保一旦条件失败，后续元素不再被处理。
- **异步安全**：通过 `pin_project` 宏正确管理异步上下文中的内存布局。

---

## 项目中的角色
该文件为 Tokio 流框架提供了 `take_while` 功能，允许用户通过条件逻辑优雅地终止流的处理。它是 Tokio 流扩展方法（如 `skip_while`、`map_while`）的重要组成部分，增强了流的灵活性和可组合性。
