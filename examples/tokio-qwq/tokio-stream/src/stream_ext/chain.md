# `chain.rs` 文件详解

## 功能概述  
该文件实现了 Tokio 流（Stream）的 `chain` 扩展方法，用于将两个流串联起来。当第一个流耗尽后，`Chain` 流会无缝切换到第二个流继续生成元素，最终形成一个连续的流。

---

## 核心组件与实现细节

### 1. `Chain` 结构体  
```rust
pin_project! {
    pub struct Chain<T, U> {
        #[pin] a: Fuse<T>,
        #[pin] b: U,
    }
}
```
- **字段说明**：
  - `a`: 使用 `Fuse<T>` 包裹的流，确保一旦耗尽就不再被轮询。
  - `b`: 第二个流，直接存储未包装的 `U` 类型。
- **作用**：通过组合两个流，实现按顺序切换流的功能。

### 2. `new` 方法  
```rust
pub(super) fn new(a: T, b: U) -> Chain<T, U> 
    where T: Stream, U: Stream 
{
    Chain { a: Fuse::new(a), b }
}
```
- **初始化逻辑**：
  - 将第一个流 `a` 包装为 `Fuse<T>`，自动处理流的熔断状态。
  - 直接存储第二个流 `b`。

### 3. `Stream` 特征实现  
```rust
impl<T, U> Stream for Chain<T, U> 
where T: Stream, U: Stream<Item=T::Item> 
{
    type Item = T::Item;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<T::Item>> {
        let me = self.project();
        if let Some(v) = ready!(me.a.poll_next(cx)) {
            return Poll::Ready(Some(v));
        }
        me.b.poll_next(cx)
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        merge_size_hints(self.a.size_hint(), self.b.size_hint())
    }
}
```
- **`poll_next` 方法逻辑**：
  1. 首先轮询 `a` 流，若仍有元素则返回。
  2. 当 `a` 耗尽后，转而轮询 `b` 流。
- **`size_hint` 方法**：合并两个流的大小提示，提供更准确的流长度估计。

---

## 在项目中的角色  
该文件为 Tokio 流框架提供了流串联的核心实现，允许开发者通过 `chain` 方法将多个流无缝连接，形成连续的数据处理链路。它是 Tokio 异步流扩展功能的重要组成部分，支持构建灵活的异步数据处理管道。

```  