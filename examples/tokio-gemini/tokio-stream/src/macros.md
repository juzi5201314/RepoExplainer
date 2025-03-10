这段代码文件定义了一系列 Rust 宏，用于根据不同的特性（features）有条件地编译代码。这些宏主要用于 `tokio-stream` 库，允许根据用户启用的特性来包含或排除特定的代码块。

具体来说，文件定义了以下宏：

*   `cfg_fs!`：如果启用了 `fs` 特性，则包含宏内部的代码。同时，在生成文档时，会添加 `#[doc(cfg(feature = "fs"))]` 属性，表明该代码块依赖于 `fs` 特性。
*   `cfg_io_util!`：如果启用了 `io-util` 特性，则包含宏内部的代码。同样，在生成文档时，会添加 `#[doc(cfg(feature = "io-util"))]` 属性。
*   `cfg_net!`：如果启用了 `net` 特性，则包含宏内部的代码。在生成文档时，会添加 `#[doc(cfg(feature = "net"))]` 属性。
*   `cfg_time!`：如果启用了 `time` 特性，则包含宏内部的代码。在生成文档时，会添加 `#[doc(cfg(feature = "time"))]` 属性。
*   `cfg_sync!`：如果启用了 `sync` 特性，则包含宏内部的代码。在生成文档时，会添加 `#[doc(cfg(feature = "sync"))]` 属性。
*   `cfg_signal!`：如果启用了 `signal` 特性，则包含宏内部的代码。在生成文档时，会添加 `#[doc(cfg(feature = "signal"))]` 属性。

这些宏的结构都非常相似，它们都接受一个代码块作为输入（用 `$($item:item)*` 表示），并使用 `#[cfg(feature = "...")]` 属性来控制代码的编译。`#[cfg_attr(docsrs, doc(cfg(feature = "...")))]` 属性用于在生成文档时，标记该代码块依赖于哪个特性。

这些宏使得库的构建过程更加灵活，允许用户根据自己的需求选择性地编译代码，从而减小二进制文件的大小，并减少不必要的依赖。例如，如果用户不需要文件系统相关的操作，就可以禁用 `fs` 特性，从而避免编译与文件系统相关的代码。
