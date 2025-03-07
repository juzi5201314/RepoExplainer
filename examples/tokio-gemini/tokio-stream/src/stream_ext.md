这个文件定义了 `StreamExt` trait，它为 `Stream` trait 提供了各种便捷的组合器函数。

**主要组成部分：**

1.  **`use` 语句**: 引入了必要的模块和 trait，包括 `core::future::Future`、`futures_core::Stream` 以及其他模块，如 `all`、`any`、`chain` 等，这些模块定义了 `StreamExt` trait 中组合器的具体实现。
2.  **`mod` 声明**: 声明了多个内部模块，这些模块包含了各种 `StreamExt` 组合器的实现细节。例如，`mod all` 包含了 `all` 组合器的实现，`mod map` 包含了 `map` 组合器的实现。
3.  **`pub use` 语句**: 将内部模块中的某些结构体或枚举导出，使得它们可以通过 `tokio_stream::stream_ext::xxx` 的方式被外部代码使用。例如，`pub use chain::Chain;` 导出了 `Chain` 结构体。
4.  **`cfg_time!` 宏**:  条件编译块，只有在启用 `time` 特征时才包含。它定义了与时间相关的组合器，如 `timeout`、`timeout_repeating`、`throttle` 和 `chunks_timeout`。
5.  **`StreamExt` trait**:  核心部分，定义了许多扩展方法，这些方法可以应用于实现了 `Stream` trait 的类型。这些方法被称为组合器，它们允许以各种方式转换、过滤和组合流。
6.  **`impl<St: ?Sized> StreamExt for St where St: Stream {}`**:  为所有实现了 `Stream` trait 的类型实现了 `StreamExt` trait，使得这些类型可以直接使用 `StreamExt` 中定义的方法。
7.  **`merge_size_hints` 函数**:  一个辅助函数，用于合并两个流的 size hint。

**`StreamExt` trait 的作用：**

*   **提供组合器**:  `StreamExt` 提供了各种组合器，用于处理和转换流。这些组合器包括：
    *   **基本操作**: `next`、`try_next`
    *   **转换**: `map`、`map_while`、`then`
    *   **合并**: `merge`、`chain`
    *   **过滤**: `filter`、`filter_map`
    *   **控制**: `fuse`、`take`、`take_while`、`skip`、`skip_while`
    *   **聚合**: `all`、`any`、`fold`、`collect`
    *   **时间相关 (如果启用 `time` 特征)**: `timeout`、`timeout_repeating`、`throttle`、`chunks_timeout`
    *   **其他**: `peekable`
*   **增强 `Stream` 的功能**:  通过提供这些组合器，`StreamExt` 极大地增强了 `Stream` trait 的功能，使得处理异步数据流更加方便和灵活。

**文件在项目中的角色：**
