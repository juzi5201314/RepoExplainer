# 代码文件 `symbol.rs` 解释

## **文件目的**
该文件定义了一个 `Symbol` 结构体，用于封装堆栈跟踪（backtrace）中的符号信息。其核心作用是：
1. 为 `BacktraceSymbol` 提供哈希（Hash）和比较（Eq/PartialEq）能力，使其可安全地存储在哈希表（如 `HashMap` 或 `HashSet`）中。
2. 通过 `parent_hash` 字段区分递归调用或相同函数在不同堆栈层级中的位置，解决单纯依赖函数名和地址无法唯一标识符号的问题。

---

## **关键组件**

### **1. `Symbol` 结构体**
```rust
pub(super) struct Symbol {
    pub(super) symbol: BacktraceSymbol,
    pub(super) parent_hash: u64,
}
```
- **字段说明**：
  - `symbol`: 来自 `backtrace` crate 的原始符号信息，包含函数名、地址、文件名、行号等。
  - `parent_hash`: 唯一标识该符号在堆栈中的层级位置，通常由父级符号的哈希值生成，确保递归调用的不同层级可被区分。

---

### **2. `Hash` Trait 实现**
```rust
impl Hash for Symbol {
    fn hash<H>(&self, state: &mut H)
    where
        H: Hasher,
    {
        // 将符号的名称、地址、文件名、行号、列号及 parent_hash 全部参与哈希计算
        // ...
    }
}
```
- **实现逻辑**：
  - 将符号的名称（`name`）、地址（`addr`）、文件名（`filename`）、行号（`lineno`）、列号（`colno`）以及 `parent_hash` 全部作为哈希输入。
  - 确保每个 `Symbol` 的哈希值唯一，即使函数名和地址相同，但 `parent_hash` 不同也会产生不同哈希。

---

### **3. `PartialEq` 和 `Eq` Trait 实现**
```rust
impl PartialEq for Symbol {
    fn eq(&self, other: &Self) -> bool {
        // 比较 parent_hash 及所有符号信息字段
        // ...
    }
}
```
- **比较逻辑**：
  - 检查 `parent_hash` 是否相等。
  - 逐项比较符号的名称、地址、文件名、行号、列号。
  - 确保只有所有字段完全一致时才视为相等。

---

### **4. `Display` Trait 实现**
```rust
impl fmt::Display for Symbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        // 格式化输出符号信息，例如：
        // "function_name at /path/to/file.rs:line:column"
        // ...
    }
}
```
- **输出格式**：
  - 显示函数名（若存在），格式化为 `::` 分隔的最后一个部分（如 `tokio::task::run` → `run`）。
  - 包含文件路径、行号和列号（若可用），便于调试时定位代码位置。

---

## **在项目中的角色**
该文件为 Tokio 运行时的任务追踪模块提供了符号信息的封装和唯一标识能力，确保堆栈跟踪（backtrace）的准确性。通过 `parent_hash` 解决递归调用的层级区分问题，并支持高效存储和比较操作，是构建完整任务执行路径追踪的核心组件。
