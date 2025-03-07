这个文件定义了一个 `Tree` 结构体，用于表示执行树的邻接表。它将 [`Trace`] 格式化为树状结构，方便展示。

**关键组件：**

*   **`Tree` 结构体：**
    *   `roots`:  一个 `HashSet`，存储树的根节点（`Symbol` 类型）。虽然代码设计允许多个根节点，但通常应该只有一个根节点。
    *   `edges`:  一个 `HashMap`，表示执行树的邻接表。键是 `Symbol`，值是 `HashSet<Symbol>`，表示该符号的子符号。
*   **`from_trace(trace: Trace) -> Self` 方法：**
    *   从 [`Trace`] 构建 `Tree`。
    *   遍历 `trace.backtraces`，将每个 backtrace 转换为 `SymbolTrace`。
    *   确定根节点，并将符号添加到 `roots`。
    *   构建 `edges` 邻接表，表示符号之间的父子关系。
*   **`consequences(&self, frame: &Symbol) -> Option<impl ExactSizeIterator<Item = &Symbol>>` 方法：**
    *   给定一个符号，返回其子符号的迭代器。
*   **`display<W: fmt::Write>(...) -> fmt::Result` 方法：**
    *   递归地将 `Tree` 格式化为文本树，并写入给定的 `fmt::Write`。
    *   使用前缀（例如 "├"、"└"）来表示树的结构。
*   **`fmt::Display for Tree` 的实现：**
    *   允许使用 `format!` 宏来格式化 `Tree`。
    *   遍历根节点，并调用 `display` 方法来打印每个子树。
*   **`to_symboltrace(backtrace: Backtrace) -> SymbolTrace` 函数：**
    *   将 `backtrace::Backtrace` 转换为 `SymbolTrace`。
    *   使用 `backtrace::Backtrace::resolve()` 解析 backtrace 中的符号。
    *   将 backtrace 中的帧转换为 `Symbol`，并按逆序累积到 `symboltrace` 中。
    *   使用哈希值来跟踪符号的父子关系。

**与其他部分的关联：**

*   `Tree` 使用 `Symbol` 类型，该类型定义在 `symbol` 模块中。
*   `Tree` 从 `Trace` 构建，`Trace` 包含 backtrace 信息。
*   `Trace` 通过 `Trace::capture`、`Trace::root` 和 `trace_leaf` 等方法进行捕获和管理。
*   `Tree` 提供了 `fmt::Display` 的实现，使得可以方便地将执行树打印出来。
