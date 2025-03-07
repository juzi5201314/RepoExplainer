这个文件定义了一个名为 `IntervalStream` 的结构体，它是一个 `tokio::time::Interval` 的包装器，实现了 `tokio_stream::Stream` trait。它的主要目的是将 `tokio::time::Interval` 转换为一个可以被 `tokio_stream` 库处理的流。

**关键组件：**

*   **`IntervalStream` 结构体:**
    *   包含一个内部的 `tokio::time::Interval` 实例 `inner`。
    *   实现了 `Debug` trait，方便调试。
    *   通过 `#[cfg_attr(docsrs, doc(cfg(feature = "time")))]` 属性，表明该结构体只有在启用 "time" 特性时才会被编译进文档。
*   **`new` 方法:**
    *   创建一个新的 `IntervalStream` 实例，接受一个 `tokio::time::Interval` 作为参数。
*   **`into_inner` 方法:**
    *   获取内部的 `tokio::time::Interval` 实例。
*   **`Stream` trait 的实现:**
    *   `type Item = Instant;`:  定义了流的每个元素是 `Instant` 类型，表示时间点。
    *   `poll_next` 方法：
        *   核心方法，用于从流中获取下一个值。
        *   调用内部 `Interval` 的 `poll_tick` 方法来获取下一个时间点。
        *   将 `poll_tick` 的结果（`Poll<Instant>`）转换为 `Poll<Option<Instant>>`，以符合 `Stream` trait 的要求。
    *   `size_hint` 方法：
        *   提供流的大小提示。
        *   这里返回 `(usize::MAX, None)`，表示流的大小未知，且可能无限。
*   **`AsRef<Interval>` 和 `AsMut<Interval>` trait 的实现:**
    *   允许通过引用访问和修改内部的 `Interval` 实例。

**如何融入项目：**

这个文件提供了一个适配器，允许开发者将 `tokio::time::Interval` 产生的定时事件转换为 `tokio_stream` 库可以处理的流。这使得开发者可以使用 `tokio_stream` 提供的各种流操作符（如 `map`, `filter`, `for_each` 等）来处理定时事件。例如，可以使用 `IntervalStream` 创建一个每隔一段时间产生一个时间戳的流，然后对这个流进行处理，比如记录日志、触发其他任务等。
