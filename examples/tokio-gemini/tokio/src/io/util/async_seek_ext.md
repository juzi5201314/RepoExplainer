这个文件定义了 `AsyncSeekExt` 特征，它为实现了 `AsyncSeek` 特征的类型添加了实用的方法。`AsyncSeek` 特征是 Tokio 异步 I/O 库中用于异步查找操作的核心特征。

**主要组成部分：**

1.  **`cfg_io_util!` 宏：** 这个宏用于条件编译，确保只有在启用了特定的特性时，`AsyncSeekExt` 特征才会被定义。这允许库根据配置选择性地包含某些功能。
2.  **`AsyncSeekExt` 特征：**
    *   这是一个扩展特征，它为实现了 `AsyncSeek` 特征的类型提供了额外的方法。
    *   它定义了 `seek` 方法，该方法用于异步地在 I/O 对象中查找指定的位置。`seek` 方法接受一个 `SeekFrom` 枚举值，该枚举值指定了查找的起始位置和偏移量。
    *   它还定义了 `rewind` 方法，这是一个便捷方法，用于将流重置到开始位置（等同于 `seek(SeekFrom::Start(0))`）。
    *   它还定义了 `stream_position` 方法，用于获取当前流的查找位置（等同于 `seek(SeekFrom::Current(0))`）。
3.  **`impl<S: AsyncSeek + ?Sized> AsyncSeekExt for S {}`：** 这是一个针对所有实现了 `AsyncSeek` 特征的类型的 `AsyncSeekExt` 特征的实现。这使得所有实现了 `AsyncSeek` 特征的类型都自动获得了 `AsyncSeekExt` 特征中定义的方法。

**与其他组件的关联：**

*   **`AsyncSeek` 特征：** `AsyncSeekExt` 特征扩展了 `AsyncSeek` 特征的功能。`AsyncSeek` 特征定义了异步查找操作的基本接口，而 `AsyncSeekExt` 特征提供了更方便的实用方法。
*   **`Seek` 结构体：** `seek` 方法返回一个 `Seek` 结构体，该结构体实现了 `Future` 特征。这允许 `seek` 操作以异步方式执行。
*   **`SeekFrom` 枚举：** `SeekFrom` 枚举用于指定查找操作的起始位置和偏移量。

**作用：**
