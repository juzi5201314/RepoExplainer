这个文件 `src/util/mod.rs` 是 `tokio-util` crate 中 `util` 模块的入口文件，它负责组织和导出 `util` 模块下的子模块和公共 API。

**主要组成部分：**

1.  **模块声明：**
    *   `mod maybe_dangling;`：声明了 `maybe_dangling` 子模块。
    *   `#[cfg(any(feature = "io", feature = "codec"))] mod poll_buf;`：条件编译声明了 `poll_buf` 子模块。只有当 `io` 或 `codec` 特性被启用时，才会编译这个模块。

2.  **公共 API 导出：**
    *   `pub(crate) use maybe_dangling::MaybeDangling;`：将 `maybe_dangling` 模块中的 `MaybeDangling` 类型导出到 crate 内部。
    *   `#[cfg(any(feature = "io", feature = "codec"))] #[cfg_attr(not(feature = "io"), allow(unreachable_pub))] pub use poll_buf::{poll_read_buf, poll_write_buf};`：条件编译导出 `poll_buf` 模块中的 `poll_read_buf` 和 `poll_write_buf` 函数。只有当 `io` 或 `codec` 特性被启用时，才会导出这些函数。`#[cfg_attr(not(feature = "io"), allow(unreachable_pub))]` 属性用于在没有 `io` 特性时，避免编译器警告。

**功能和作用：**

*   **模块组织：** 组织了 `tokio-util` crate 中与实用工具相关的代码。
*   **条件编译：** 使用 `cfg` 属性，根据不同的特性（`io` 和 `codec`）来控制模块的编译和 API 的导出，实现代码的模块化和按需编译。
*   **API 导出：** 提供了对 `util` 模块中关键类型和函数的访问，使得其他模块可以方便地使用这些工具。
