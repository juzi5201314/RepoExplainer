# `filter_map.rs` 文件解析

## 文件目的
该文件实现了 Tokio 异步流库中 `filter_map` 方法的核心逻辑。通过组合过滤和映射功能，允许用户对流中的元素进行条件转换，仅保留满足闭包条件的元素。

## 关键组件

### 1. `FilterMap` 结构体
```rust
pin_project! {
    pub struct FilterMap<St, F> {
        #[pin]
        stream: St,
        f: F,
    }
}
```
- **功能**：包装原始流 `St` 和闭包 `F`，实现过滤映射逻辑。
- **特性**：
  - 使用 `pin_project` 宏处理内部 `Pin` 安全性，确保 `stream` 字段被正确钉选。
  - 实现 `Debug` trait，方便调试时展示内部流状态。

### 2. `Stream` Trait 实现
```rust
impl<St, F, T> Stream for FilterMap<St, F>
where
    St: Stream,
    F: FnMut(St::Item) -> Option<T>,
{
    // ...
}
```
- **核心方法**：
  - `poll_next`：
    ```rust
    fn poll_next(...) -> Poll<Option<T>> {
        loop {
            match ready!(self.project().stream.poll_next(cx)) {
                Some(e) => {
                    if let Some(e) = (self.project().f)(e) {
                        return Poll::Ready(Some(e));
                    }
                }
                None => return Poll::Ready(None),
            }
        }
    }
    ```
    - **逻辑**：持续轮询底层流，对每个元素应用闭包 `f`：
      - 若返回 `Some`，则保留该元素；
      - 若返回 `None`，则跳过当前元素继续轮询；
      - 流结束时返回 `None`。
    - 使用 `ready!` 宏处理异步就绪状态，确保正确暂停/恢复。
  - `size_hint`：
    ```rust
    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, self.stream.size_hint().1)
    }
    ```
    - 由于过滤条件可能减少元素数量，下界设为 `0`，上界继承原始流的上界。

## 与其他结构体的关联
通过对比相关上下文中的其他结构体（如 `Filter`、`MapWhile` 等）：
- **功能差异**：`filter_map` 同时实现过滤和映射，而 `Filter` 仅过滤，`Map` 仅映射。
- **实现模式**：均通过 `pin_project` 宏定义结构体，并实现 `Stream` Trait，体现 Tokio 流扩展方法的统一设计模式。

## 在项目中的角色