# `map.rs` 文件详解

## 概述
该文件实现了 Tokio 异步流的 `map` 方法扩展，通过 `Map` 结构体为流提供元素转换功能。它属于 `tokio-stream` 库中 `StreamExt` 特性扩展的一部分，用于在不阻塞事件循环的情况下对异步流进行数据转换。

---

## 核心组件

### 1. `Map` 结构体
```rust
pin_project! {
    pub struct Map<St, F> {
        #[pin]
        stream: St,
        f: F,
    }
}
```
- **功能**：包装原始流 `St` 和转换函数 `F`，实现对流元素的逐项映射。
- **关键特性**：
  - 使用 `pin_project` 宏管理内部 `Pin` 安全性，确保 `stream` 字段被正确 `pin`。
  - `#[pin]` 标记的 `stream` 字段表示其需要被 `pin` 到固定内存位置，符合异步流的生命周期要求。

---

### 2. 调试支持
```rust
impl<St, F> fmt::Debug for Map<St, F>
where
    St: fmt::Debug,
{
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Map").field("stream", &self.stream).finish()
    }
}
```
- **作用**：提供调试信息输出能力，通过显示内部流的状态辅助调试。

---

### 3. 构造方法
```rust
pub(super) fn new(stream: St, f: F) -> Self {
    Map { stream, f }
}
```
- **功能**：创建新的 `Map` 实例，接受原始流和转换函数作为参数。

---

### 4. `Stream` 特性实现
```rust
impl<St, F, T> Stream for Map<St, F>
where
    St: Stream,
    F: FnMut(St::Item) -> T,
{
    type Item = T;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<T>> {
        self.as_mut()
            .project()
            .stream
            .poll_next(cx)
            .map(|opt| opt.map(|x| (self.as_mut().project().f)(x)))
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        self.stream.size_hint()
    }
}
```
- **核心逻辑**：
  - **`poll_next`**：驱动流的异步轮询，对原始流返回的每个元素应用转换函数 `f`。
  - **`size_hint`**：直接继承原始流的大小提示，保持一致性。
- **关键操作**：
  - 使用 `project()` 方法安全地解构 `Pin` 对象，访问内部字段。
  - 通过 `map` 组合操作符链式处理轮询结果和函数应用。

---

## 与其他组件的关系
该文件与 Tokio 流处理生态中的其他结构体（如 `MapWhile`、`Take`、`FilterMap`）并列，共同构成流操作符集合。这些结构体通过组合 `pin_project` 和 `Stream` 特性实现，提供类似迭代器适配器的异步流处理能力。

---

## 项目中的角色