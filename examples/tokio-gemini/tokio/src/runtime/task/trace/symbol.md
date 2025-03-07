这个文件定义了一个名为 `Symbol` 的结构体，用于表示回溯信息中的一个符号。它主要用于在 Tokio 运行时中跟踪任务的执行情况。

**关键组件：**

*   **`Symbol` 结构体：**
    *   `symbol`:  一个 `backtrace::BacktraceSymbol` 类型的字段，它封装了来自 `backtrace` crate 的原始符号信息，例如函数名、地址、文件名、行号和列号。
    *   `parent_hash`:  一个 `u64` 类型的字段，用于标识该符号在其回溯跟踪中的位置。这对于区分递归调用等情况非常重要，因为相同的函数可能在不同的调用深度出现。

*   **`Hash` trait 的实现：**
    *   实现了 `Hash` trait，使得 `Symbol` 结构体可以被用作哈希表的键。
    *   哈希计算基于符号的名称（如果存在）、地址（如果存在）、文件名、行号、列号和 `parent_hash`。

*   **`PartialEq` 和 `Eq` trait 的实现：**
    *   实现了 `PartialEq` 和 `Eq` trait，使得 `Symbol` 结构体可以进行比较。
    *   比较逻辑考虑了 `parent_hash`、符号名称（如果存在）、地址（如果存在）、文件名、行号和列号。

*   **`fmt::Display` trait 的实现：**
    *   实现了 `fmt::Display` trait，使得 `Symbol` 结构体可以被格式化为字符串。
    *   格式化输出包括函数名（简化处理，移除最后的 `::` 及其后的内容）、文件名、行号和列号。

**功能和作用：**

这个文件定义了 `Symbol` 结构体，它对 `backtrace::BacktraceSymbol` 进行了封装，并添加了 `parent_hash` 字段。这使得 `Symbol` 结构体可以被安全地用作哈希表的键，并且能够区分递归调用等情况。`Symbol` 结构体还实现了 `Display` trait，方便进行调试和日志输出。这些功能共同构成了 Tokio 运行时中任务跟踪的基础，帮助开发者理解任务的执行流程和性能瓶颈。
