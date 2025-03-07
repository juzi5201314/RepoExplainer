# 文件说明：empty.rs

## 目的
该文件实现了 Tokio 流库中的 `empty` 空流功能。提供一个立即完成且不产生任何元素的流，用于需要空流的异步场景。

## 关键组件

### 1. `Empty<T>` 结构体
```rust
pub struct Empty<T>(PhantomData<T>);
```
- 使用 `PhantomData<T>` 占位符保持类型参数 T 的关联性
- 实现了 `Unpin`、`Send`、`Sync` trait，确保该流可以在不同场景下安全使用
- 通过 `Debug` trait 提供调试信息

### 2. `empty` 工厂函数
```rust
pub const fn empty<T>() -> Empty<T> {
    Empty(PhantomData)
}
```
- 通过 `const fn` 实现编译时常量初始化
- 返回一个立即完成的空流实例
- 文档明确说明与 `pending()` 的区别：`empty` 立即返回 `None`，而 `pending` 永远不就绪

### 3. Stream trait 实现
```rust
impl<T> Stream for Empty<T> {
    type Item = T;

    fn poll_next(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<Option<T>> {
        Poll::Ready(None)
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, Some(0))
    }
}
```
- `poll_next` 直接返回 `Poll::Ready(None)` 表示流立即完成
- `size_hint` 明确说明流长度为 0
- 通过 `Pin` 处理不可变借用的移动语义

## 项目中的角色