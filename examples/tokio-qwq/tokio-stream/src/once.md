# 文件说明：`once.rs`

## 文件目的
该文件实现了 Tokio 流库中的 `once` 函数，提供一个只产生单次元素的异步流。该流在初始化时立即就绪，仅在第一次轮询时返回指定值，后续轮询返回 `None`。

## 核心组件

### 1. `Once<T>` 结构体
```rust
pub struct Once<T> {
    iter: Iter<option::IntoIter<T>>,
}
```
- **功能**：表示单次流的内部状态
- **关键特性**：
  - 通过 `Iter` 适配器包装 `Option<T>` 的迭代器
  - 实现 `Unpin` trait 允许在需要移动所有权的场景中使用
  - `#[must_use]` 属性强制开发者必须轮询该流

### 2. `once` 工厂函数
```rust
pub fn once<T>(value: T) -> Once<T> {
    Once { iter: crate::iter(Some(value)) }
}
```
- **功能**：创建单次流实例
- **实现细节**：
  - 将输入值包装在 `Some(value)` 中
  - 通过 `crate::iter` 转换为迭代器驱动的流
  - 示例展示了如何获取单次值并验证后续轮询结果

### 3. Stream Trait 实现
```rust
impl<T> Stream for Once<T> {
    fn poll_next(...) { Pin::new(&mut self.iter).poll_next(cx) }
    fn size_hint(&self) { self.iter.size_hint() }
}
```
- **关键方法**：
  - `poll_next` 委托给内部迭代器的轮询逻辑
  - `size_hint` 直接返回迭代器的容量信息
- **行为特性**：
  - 第一次轮询返回初始值
  - 后续轮询立即返回 `Poll::Ready(None)`

## 项目中的角色
该文件为 Tokio 流库提供了基础构建块，通过 `once` 函数实现单次值流的创建，是构建更复杂流结构的重要基础组件。其简洁的设计完美适配异步场景中需要单次值传递的常见需求。
