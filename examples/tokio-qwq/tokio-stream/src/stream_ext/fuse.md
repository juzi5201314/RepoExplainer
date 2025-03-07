# `tokio-stream/src/stream_ext/fuse.rs` 文件解析

## 文件目的
该文件实现了 Tokio 异步流（Stream）的 `fuse` 扩展功能。Fuse 机制确保流在首次完成（返回 `None`）后不再被轮询，避免因重复轮询已结束的流导致的逻辑错误。

---

## 核心组件

### 1. `Fuse<T>` 结构体
```rust
pin_project! {
    pub struct Fuse<T> {
        #[pin]
        stream: Option<T>,
    }
}
```
- **功能**：包装原始流 `T`，通过 `Option<T>` 记录流是否已耗尽。
- **关键特性**：
  - 使用 `pin_project` 宏处理 Pin 语义，确保结构体正确支持异步操作。
  - `stream` 字段被标注为 `pin`，表明其需要被 Pin 语法处理。

---

### 2. `Fuse<T>` 实现细节

#### 构造方法
```rust
pub(crate) fn new(stream: T) -> Fuse<T> {
    Fuse { stream: Some(stream) }
}
```
- 初始化时将原始流包装在 `Some` 中，表示流处于可轮询状态。

---

#### `Stream` 特性实现
```rust
impl<T> Stream for Fuse<T> where T: Stream {
    // ...
}
```

#### `poll_next` 方法
```rust
fn poll_next(...) -> Poll<Option<T::Item>> {
    // 轮询内部流
    let res = match self.project().stream.as_pin_mut() {
        Some(stream) => ready!(stream.poll_next(cx)),
        None => return Poll::Ready(None),
    };

    // 若流已耗尽，标记为 None
    if res.is_none() {
        self.project().stream.set(None);
    }
    Poll::Ready(res)
}
```
- **流程**：
  1. 若 `stream` 存在，正常轮询原始流。
  2. 若轮询结果为 `None`（流结束），将 `stream` 置为 `None`。
  3. 后续调用直接返回 `None`，不再触发起始流。
- **作用**：确保流仅被轮询至首次完成。

#### `size_hint` 方法
```rust
fn size_hint(&self) -> (usize, Option<usize>) {
    match &self.stream {
        Some(s) => s.size_hint(),
        None => (0, Some(0)),
    }
}
```
- 返回剩余元素的大小提示，若流已耗尽则返回 `(0, Some(0))`。

---

## 在项目中的角色
该文件为 Tokio 的流提供了 `fuse` 扩展，通过封装流的轮询逻辑，确保流在首次完成时停止后续操作，是异步编程中安全处理流状态的重要工具。
