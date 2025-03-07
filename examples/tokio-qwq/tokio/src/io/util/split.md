### 文件说明：`split.rs`

#### 文件目的
该文件实现了 Tokio 的 `AsyncBufRead` 类型的分片功能，允许将基于缓冲的异步读取操作拆分为以指定分隔符分隔的段，并通过流（Stream）形式逐段处理。这是处理网络或文件 I/O 中分隔符分隔数据（如行分割或消息分隔）的核心组件。

---

#### 关键组件

1. **`Split` 结构体**
   - **定义**：通过 `pin_project_lite` 宏生成，包含以下字段：
     - `reader`: 被拆分的异步缓冲读取对象（`AsyncBufRead`）。
     - `buf`: 内部缓冲区，存储读取到的数据。
     - `delim`: 分隔符字节。
     - `read`: 已读取的字节数（辅助状态跟踪）。
   - **功能**：跟踪读取进度，管理缓冲区，并提供分片逻辑。

2. **`split` 工厂函数**
   - **作用**：创建 `Split` 实例，初始化缓冲区和分隔符。
   - **参数**：`reader`（异步缓冲读取对象）和 `delim`（分隔符字节）。

3. **`next_segment` 方法**
   - **功能**：返回下一个分片的异步 Future。
   - **实现**：通过 `poll_fn` 将 `poll_next_segment` 封装为 Future，驱动异步轮询。

4. **`poll_next_segment` 方法**
   - **核心逻辑**：
     1. 调用 `read_until_internal` 读取数据直到遇到分隔符。
     2. 处理缓冲区：若分隔符存在则移除，并返回当前缓冲区内容。
     3. 返回结果：`Poll::Ready`（成功或结束）或 `Poll::Pending`（等待数据）。
   - **状态管理**：通过 `mem::take` 将缓冲区内容转移为结果，确保状态正确重置。

5. **测试**
   - **`assert_unpin`**：验证 `Split` 实现 `Unpin`，确保其可安全用于异步上下文。

---

#### 工作流程
1. **初始化**：通过 `split(reader, delim)` 创建 `Split` 实例。
2. **异步读取**：调用 `next_segment().await` 触发异步读取，直到遇到分隔符。
3. **分片处理**：每次调用返回一个包含当前段的 `Vec<u8>`，直到读取完成返回 `None`。

---

#### 与项目其他部分的关联
- **`SplitStream`**：该文件的 `Split` 结构体是 `SplitStream` 的内部实现基础。`SplitStream` 通过包装 `Split` 实现 `Stream` 特性，允许通过 `for await` 等流式语法处理分片。
- **`read_until_internal`**：依赖 `read_until` 模块的内部函数，负责底层的异步读取逻辑。

---

#### 文件在项目中的角色