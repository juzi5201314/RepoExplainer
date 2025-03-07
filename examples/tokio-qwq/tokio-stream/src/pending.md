# 文件说明：`pending.rs`

## 目的
该文件实现了 Tokio 流库中的一个特殊流类型 `Pending<T>`，用于创建一个永远不会产生元素的无限等待流。它提供了一个标准化的惰性流实现，适用于需要阻塞或无限等待的场景。

## 关键组件

### 1. `Pending<T>` 结构体
```rust
pub struct Pending<T>(PhantomData<T>);
```
- 使用 `PhantomData<T>` 保持类型关联，但实际不存储任何数据
- 通过 `#[must_use = "streams do nothing unless polled"]` 标记强制用户必须轮询该流
- 实现了以下标记特征：
  - `Unpin`：表明该结构体在移动时不需要重新 Pin
  - `Send`/`Sync`：允许安全跨线程传递和共享

### 2. `pending` 函数
```rust
pub const fn pending<T>() -> Pending<T> {
    Pending(PhantomData)
}
```
- 零成本构造 `Pending<T>` 实例的工厂函数
- 返回的流永远不会准备好，调用 `next().await` 会无限阻塞
- 与 `stream::empty()` 的区别：后者立即完成但无元素，而 `pending` 永远不完成

### 3. Stream 特征实现
```rust
impl<T> Stream for Pending<T> {
    type Item = T;

    fn poll_next(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<Option<T>> {
        Poll::Pending
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, None)
    }
}
```
- `poll_next` 总是返回 `Poll::Pending`，表示流永远不就绪
- `size_hint` 明确表示流不会产生任何元素（0 最小值），但可能无限期等待（无最大值）

## 在项目中的作用
该文件为 Tokio 流库提供了基础的惰性流实现，用于需要无限等待的场景。通过标准化的 `Pending` 流，开发者可以：
1. 在测试中模拟永远不完成的流
2. 在控制流中创建阻塞点
3. 与其他流组合实现特定逻辑（如超时处理）

作为 Tokio 流组件的重要组成部分，它为异步编程提供了必要的基础构建块，帮助开发者处理各种边缘情况。

### 文件角色