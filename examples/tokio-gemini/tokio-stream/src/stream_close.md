这个文件定义了一个名为 `StreamNotifyClose` 的结构体，它是一个 `Stream` 的包装器。它的主要目的是在底层 `Stream` 结束时，通知上层该 `Stream` 已经关闭。

**关键组件：**

*   `StreamNotifyClose<S>`:  一个结构体，它包装了一个实现了 `Stream` trait 的类型 `S`。它使用 `pin_project` 宏来确保 `inner` 字段（即被包装的 `Stream`）可以被安全地固定。
*   `inner: Option<S>`:  一个 `Option`，它持有被包装的 `Stream`。当底层 `Stream` 结束时，`inner` 会被设置为 `None`，表示 `Stream` 已经关闭。
*   `new(stream: S)`:  一个关联函数，用于创建一个新的 `StreamNotifyClose` 实例，并将给定的 `Stream` 包装起来。
*   `into_inner(self) -> Option<S>`:  一个方法，用于获取被包装的 `Stream`。如果 `Stream` 已经结束，则返回 `None`。
*   `poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>>`:  实现了 `Stream` trait 的 `poll_next` 方法。它首先检查 `inner` 是否为 `Some`。如果是，则调用底层 `Stream` 的 `poll_next` 方法。如果底层 `Stream` 产生一个 `Some(item)`，则 `StreamNotifyClose` 也会产生一个 `Some(Some(item))`。如果底层 `Stream` 产生一个 `None`，则 `StreamNotifyClose` 会先产生一个 `Some(None)`，然后将 `inner` 设置为 `None`，表示 `Stream` 已经关闭。如果 `inner` 为 `None`，则直接返回 `Poll::Ready(None)`。
*   `size_hint(&self) -> (usize, Option<usize>)`:  实现了 `Stream` trait 的 `size_hint` 方法。它返回底层 `Stream` 的 `size_hint`，并根据 `Stream` 是否存在，调整返回值。

**工作原理：**

`StreamNotifyClose` 包装了另一个 `Stream`。当被包装的 `Stream` 产生一个值时，`StreamNotifyClose` 也会产生这个值，并用 `Some` 包装。当被包装的 `Stream` 结束时，`StreamNotifyClose` 会首先产生一个 `None`，然后自身结束。这使得上层代码可以知道底层 `Stream` 已经关闭。

**与项目的关系：**

这个文件定义了一个用于包装其他 `Stream` 的适配器，它允许上层代码检测底层 `Stream` 的关闭状态。这在需要处理多个 `Stream` 的场景中非常有用，例如 `StreamMap`，它需要知道每个 `Stream` 何时关闭。
