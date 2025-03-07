这个文件 `support.rs` 包含了一些 Tokio 库中常用的类型和宏的导入和定义，为 Tokio 库的其他部分提供了支持。

**主要组成部分：**

1.  **`cfg_macros!` 宏块:**
    *   这个宏块根据编译配置条件 (`cfg_macros!`) 包含了一些 `pub use` 语句，用于将其他模块中的特定项导出到当前模块。
    *   `pub use crate::future::maybe_done::maybe_done;`: 导入 `maybe_done`，可能是一个用于处理可能完成的 Future 的结构体或函数。
    *   `pub use std::future::poll_fn;`: 导入 `poll_fn`，一个用于创建 Future 的函数，它接受一个闭包，该闭包负责轮询 Future。
    *   `#[doc(hidden)] pub fn thread_rng_n(n: u32) -> u32 { ... }`:  定义了一个隐藏的函数 `thread_rng_n`，用于生成随机数。它调用了 `crate::runtime::context::thread_rng_n(n)`，这表明它与 Tokio 的运行时上下文有关。

2.  **`pub use` 语句:**
    *   `pub use std::future::{Future, IntoFuture};`: 导入标准库中的 `Future` 和 `IntoFuture` trait，它们是异步编程的核心。
    *   `pub use std::pin::Pin;`: 导入 `Pin` 类型，用于固定 Future 和其他类型在内存中的位置，这对于安全地处理自引用结构至关重要。
    *   `pub use std::task::Poll;`: 导入 `Poll` 枚举，用于表示 Future 的轮询状态（`Ready` 或 `Pending`）。

**与其他文件的关系：**

*   这个文件通过 `pub use` 语句，将 Tokio 库中常用的类型和函数导出，供其他模块使用。
*   `thread_rng_n` 函数与 Tokio 的运行时上下文相关，可能用于在运行时生成随机数。
*   `maybe_done` 和 `poll_fn` 提供了处理 Future 的工具。

**总结：**
