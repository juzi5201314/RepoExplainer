# 文件说明：`tokio/src/macros/join.rs`

## **文件目的**
该文件定义了 Tokio 框架中的 `join!` 宏，用于在异步任务中并发执行多个异步表达式（future），并等待所有分支完成后返回结果。它是 Tokio 异步编程的核心并发控制工具之一。

---

## **关键组件与实现细节**

### **1. 文档生成宏 `doc!`**
- **功能**：通过宏生成 `join!` 的文档注释。
- **内容**：
  - **核心说明**：`join!` 必须在异步函数/闭包中使用，将多个异步表达式转换为 future 并并发执行。
  - **错误处理**：即使某些分支返回 `Err`，仍会等待所有分支完成；若需提前终止，需使用 `try_join!`。
  - **性能特性**：不分配 `Vec`，直接内联存储 future。
  - **运行时特性**：所有分支在**同一任务**中执行，因此并发但非并行（无法跨线程执行）。若需并行，需通过 `tokio::spawn` 创建任务后再传入 `join!`。
  - **示例**：展示如何在 `main` 函数中使用 `join!` 并发执行两个异步函数。

### **2. `join!` 宏实现**
- **结构**：
  - **入口点**：`( $($e:expr),+ $(,)? )` 处理输入的异步表达式列表。
  - **归一化处理**：通过 `@` 标记的嵌套模式匹配，统计分支数量并生成内部结构。
  - **核心逻辑**：
    - 使用 `poll_fn` 和 `Pin` 管理 future 的轮询（polling）。
    - 通过 `skip_next_time` 变量控制轮询顺序，确保每个 future 都有机会执行（避免被其他 future 占用全部执行时间）。
    - 若所有 future 完成，返回结果元组；否则标记为 pending。
  - **空分支处理**：`()` 时直接执行空异步块。

### **3. 低层工具**
- **`maybe_done`**：将表达式转换为可轮询的 future。
- **`Pin`**：确保 future 在栈上固定，避免移动导致的悬垂指针问题。
- **轮询策略**：采用双循环策略，首次跳过部分 future，确保公平调度。

---

## **与其他组件的关联**
- **`try_join!`**：功能类似但遇到 `Err` 时提前终止，需通过 `doc` 上下文中的对比说明。
- **`tokio::spawn`**：用于创建独立任务以实现并行执行，需在文档中指导用户如何结合使用。
- **`JoinSet`**：提供更灵活的多任务管理，适合无需严格结果顺序的场景。

---

## **在项目中的角色**
此文件通过 `join!` 宏为 Tokio 提供了在单任务内并发执行多个异步操作的核心能力，支持高效管理异步分支的协同执行，是 Tokio 异步编程模型的重要组成部分。
