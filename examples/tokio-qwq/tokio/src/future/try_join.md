### 文件说明：`tokio/src/future/try_join.rs`

#### 目的
该文件实现了 `TryJoin3` 组合器，用于并行执行三个 `Future`，并在所有 `Future` 成功完成后返回结果元组，若其中任何一个 `Future` 失败则立即返回错误。

---

#### 关键组件

1. **`try_join3` 函数**
   - **功能**：接受三个 `Future` 参数，返回 `TryJoin3` 结构体实例。
   - **参数要求**：三个 `Future` 的输出类型必须是 `Result<T, E>`。
   - **初始化**：将每个 `Future` 包装为 `MaybeDone` 类型以跟踪其完成状态。

2. **`TryJoin3` 结构体**
   - **定义**：通过 `pin_project!` 宏实现 `Pin` 安全投影，包含三个 `MaybeDone` 包装的 `Future`。
   - **字段**：
     ```rust
     #[pin] future1: MaybeDone<F1>,
     #[pin] future2: MaybeDone<F2>,
     #[pin] future3: MaybeDone<F3>,
     ```
   - **作用**：管理三个异步任务的状态，并协调它们的完成逻辑。

3. **`Future` 特征实现**
   - **`poll` 方法**：
     - **流程**：
       1. 轮询每个 `Future` 的状态。
       2. 若任一 `Future` 处于 `Pending`，标记 `all_done` 为 `false`。
       3. 若任一 `Future` 返回 `Err`，立即返回该错误。
       4. 若所有 `Future` 成功完成，返回结果元组。
     - **错误处理**：一旦检测到错误，直接终止并返回第一个错误。
     - **结果收集**：所有成功时，从 `MaybeDone` 中提取值并组合为元组。

---

#### 工作原理
1. **初始化**：通过 `maybe_done` 将每个 `Future` 封装为 `MaybeDone`，以便跟踪其完成状态。
2. **轮询逻辑**：
   - 每次 `poll` 调用时，依次检查三个 `Future` 的状态。
   - 若所有 `Future` 完成且成功，则返回结果元组。
   - 若任一 `Future` 失败，立即返回错误。
3. **状态管理**：利用 `MaybeDone` 存储已完成的 `Future` 的结果，避免重复轮询。

---

#### 项目中的角色