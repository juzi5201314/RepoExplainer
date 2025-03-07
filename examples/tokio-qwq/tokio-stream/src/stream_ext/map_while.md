# `map_while.rs` 文件详解

## 文件目的
该文件实现了 Tokio 流（Stream）的 `map_while` 扩展方法，提供一种在流处理过程中动态转换元素并终止流的功能。当提供的闭包返回 `None` 时，流将提前终止，否则继续处理元素。

---

## 核心组件

### 1. `MapWhile` 结构体
```rust
pin_project! {
    pub struct MapWhile<St, F> {
        #[pin]
        stream: St,
        f: F,
    }
}
```
- **功能**：包装原始流和转换闭包，实现 `map_while` 行为。
- **字段**：
  - `stream`: 被包装的原始流（使用 `#[pin]` 标记以支持 Pin 语义）。
  - `f`: 用户提供的闭包，类型为 `FnMut(St::Item) -> Option<T>`。

---

### 2. 实现 `Stream` 特征
```rust
impl<St, F, T> Stream for MapWhile<St, F>
where
    St: Stream,
    F: FnMut(St::Item) -> Option<T>,
{
    type Item = T;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<T>> {
        me.stream.poll_next(cx).map(|opt| opt.and_then(f))
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, self.stream.size_hint().1)
    }
}
```
- **`poll_next` 方法**：
  - 调用底层流的 `poll_next` 获取元素。
  - 使用 `and_then` 将闭包 `f` 应用于元素：若 `f` 返回 `Some(T)`，则继续；若返回 `None`，流终止。
- **`size_hint` 方法**：
  - 下界设为 `0`，因为闭包可能提前终止流，无法保证最小元素数量。
  - 上界继承自原始流。

---

### 3. 辅助实现
- **`Debug` 特征**：通过 `fmt::Debug` 为结构体提供调试输出，展示内部流的信息。
- **`new` 构造函数**：创建 `MapWhile` 实例，接受原始流和闭包。

---

## 工作原理
1. **流转换**：每次轮询原始流的下一个元素。
2. **闭包应用**：将元素传递给用户提供的闭包 `f`。
3. **终止条件**：若闭包返回 `None`，流立即终止；否则返回转换后的值。
4. **异步协作**：通过 `Pin` 和 `poll_next` 实现异步安全的流处理。

---

## 项目中的角色
该文件为 Tokio 流框架提供了 `map_while` 方法的实现，允许用户在流处理过程中动态转换元素并根据条件提前终止流，是 Tokio 异步流处理功能的重要扩展组件。
