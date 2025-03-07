# 文件说明：`tree.rs`

## 文件目的  
该文件定义了 `Tree` 结构体及其相关方法，用于将 Tokio 运行时的任务执行轨迹（`Trace`）转换为树形结构，并提供可视化输出功能。它是 Tokio 任务跟踪系统中用于执行路径可视化的关键中间表示层。

---

## 核心组件与功能

### 1. `Tree` 结构体  
```rust
pub(super) struct Tree {
    roots: HashSet<Symbol>,
    edges: HashMap<Symbol, HashSet<Symbol>>,
}
```
- **数据结构**：
  - `roots`：存储树的根节点集合（理论上应只有一个根节点，但代码支持多根情况）。
  - `edges`：邻接表表示的树结构，键为父节点 `Symbol`，值为子节点集合。
- **功能**：
  - 将线性 `Trace` 转换为树形结构，便于后续格式化输出。
  - 支持递归遍历和可视化展示。

---

### 2. 核心方法

#### (1) `from_trace`：从 `Trace` 构建树  
```rust
pub(super) fn from_trace(trace: Trace) -> Self { ... }
```
- **流程**：
  1. 遍历 `Trace` 中的每个 `Backtrace`。
  2. 调用 `to_symboltrace` 将 `Backtrace` 转换为 `SymbolTrace`（符号化路径）。
  3. 提取路径首节点作为根节点。
  4. 构建邻接表：对路径中每一对连续符号（父节点和子节点），在 `edges` 中记录父子关系。

#### (2) `display`：树形结构可视化  
```rust
fn display<W: fmt::Write>(&self, f: &mut W, root: &Symbol, is_last: bool, prefix: &str) -> fmt::Result { ... }
```
- **功能**：
  - 使用递归方式遍历树节点，生成带缩进的文本树。
  - 使用符号 `└╼` 和 `├╼` 表示分支，通过 `prefix` 参数控制缩进层级。
  - 支持多根节点的并列展示。

#### (3) `to_symboltrace`：符号化路径转换  
```rust
fn to_symboltrace(backtrace: Backtrace) -> SymbolTrace { ... }
```
- **流程**：
  1. 解析 `Backtrace` 中的帧，获取符号信息。
  2. 反转帧顺序（确保从栈底到栈顶的执行路径）。
  3. 为每个符号生成唯一 `parent_hash`（基于哈希链）以记录层级关系。

---

### 3. `Symbol` 类型  
（定义在 `symbol.rs` 中，此处通过导入使用）  
- **字段**：
  - `symbol`: 具体符号信息（如函数名、地址等）。
  - `parent_hash`: 父节点的哈希值，用于唯一标识符号在树中的位置。

---

## 在项目中的作用  
该文件是 Tokio 运行时任务跟踪模块的核心组件，主要负责以下功能：
1. **轨迹转换**：将线性执行路径（`Trace`）转换为树形结构，便于展示任务执行的分支与嵌套关系。
2. **可视化输出**：通过 `Display` trait 提供可读性强的树状文本，用于调试或日志记录，帮助开发者理解任务调度和执行流程。
3. **中间表示层**：作为 `Trace` 和最终输出格式之间的桥梁，解耦数据存储与展示逻辑。

---

## 文件角色总结  