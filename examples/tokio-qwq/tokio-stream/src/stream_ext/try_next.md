### 代码文件解释

#### 目的
该文件实现了 `tokio-stream` 库中 `StreamExt` trait 的 `try_next` 方法，用于从异步流中安全地获取下一个元素。该方法专门处理流项为 `Result<T, E>` 类型的场景，允许在遇到错误时立即终止操作。

#### 关键组件
1. **结构体 `TryNext`**
   - **定义**：通过 `pin_project` 宏生成，包含以下字段：
     - `inner`: 嵌套的 `Next` 结构体，负责实际的流轮询操作。
     - `_pin`: 使用 `PhantomPinned` 确保该 future 实现 `!Unpin`，以兼容异步 trait 方法。
   - **特性**：
     - Cancel-safe：仅持有流的引用，不会因丢弃而丢失数据。
     - 实现 `Future` trait，输出类型为 `Result<Option<T>, E>`。

2. **`new` 方法**
   - 初始化 `TryNext` 实例，通过 `Next::new` 创建内部状态。

3. **`Future` 实现**
   - **`poll` 方法**：
     - 调用 `inner` 的 `poll` 获取流的下一个项。
     - 使用 `Option::transpose()` 将 `Option<Result<T, E>>` 转换为 `Result<Option<T>, E>`，使错误优先返回。

#### 工作原理
- 当调用 `stream.try_next()` 时，返回一个 `TryNext` future。
- 轮询该 future 时：
  1. 调用底层流的 `poll_next` 获取项。
  2. 若流项为 `Ok(value)`，返回 `Ok(Some(value))`。
  3. 若流项为 `Err(e)`，返回 `Err(e)` 并终止后续操作。
  4. 若流已耗尽，返回 `Ok(None)`。

#### 项目中的角色