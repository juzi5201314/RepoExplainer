# `stream_close.rs` 文件解析

## 文件目的
该文件实现了 `StreamNotifyClose` 结构体，用于在流结束时显式通知消费者。它通过将原始流的每个元素包裹在 `Some` 中，并在流结束后额外发出一个 `None` 值，从而区分正常元素和流关闭事件。

## 核心组件

### 1. `StreamNotifyClose<S>` 结构体
```rust
pin_project! {
    pub struct StreamNotifyClose<S> {
        #[pin]
        inner: Option<S>,
    }
}
```
- **功能**：包装原始流 `S`，在流结束后追加一个 `None` 元素。
- **字段**：
  - `inner`: 使用 `Option<S>` 存储原始流，当流结束时设置为 `None`。

### 2. 方法实现
#### 构造方法
```rust
pub fn new(stream: S) -> Self {
    Self { inner: Some(stream) }
}
```
初始化时将原始流包裹在 `Some` 中。

#### 转换方法
```rust
pub fn into_inner(self) -> Option<S> {
    self.inner
}
```
释放内部流（若未结束则返回 `Some`，否则返回 `None`）。

### 3. `Stream` 特性实现
#### `poll_next` 方法
```rust
fn poll_next(...) -> Poll<Option<Self::Item>> {
    match self.as_mut().project().inner.as_pin_mut().map(|stream| S::poll_next(stream, cx)) {
        Some(Poll::Ready(None)) => { 
            self.project().inner.set(None); 
            Poll::Ready(Some(None)) 
        },
        ...
    }
}
```
- **逻辑**：
  - 当原始流结束时（返回 `Poll::Ready(None)`），设置 `inner` 为 `None`，并返回 `Some(None)`。
  - 正常元素时返回 `Some(Some(item))`。
  - 流完全结束后返回 `None`。

#### `size_hint` 方法
```rust
fn size_hint(&self) -> (usize, Option<usize>) {
    if let Some(inner) = &self.inner {
        let (l, u) = inner.size_hint();
        (l.saturating_add(1), u.and_then(|u| u.checked_add(1)))
    } else {
        (0, Some(0))
    }
}
```
- 在原始流的大小提示基础上加 `1`，表示额外的 `None` 元素。

## 使用场景
通过示例代码可见，该结构体常与 `StreamMap` 配合使用：
```rust
let stream = StreamNotifyClose::new(tokio_stream::iter(vec![0, 1]));
map.insert(0, stream);
...
match val {
    Some(val) => println!("收到值"),
    None => println!("流已关闭"),
}
```
允许在处理多个流时区分元素到达和流关闭事件。

## 项目中的角色