### 文件解释

#### 目的
该文件实现了 Tokio 异步 I/O 框架中的 `read_until` 功能，用于从异步缓冲流中读取数据直到遇到指定分隔符，并将结果存储到 `Vec<u8>` 中。该功能是 `AsyncBufReadExt` trait 的核心实现之一，支持非阻塞的分隔符驱动数据读取。

#### 关键组件
1. **`ReadUntil` 结构体**
   - **字段**：
     - `reader`: 引用外部异步缓冲读取器（实现 `AsyncBufRead` trait）
     - `delimiter`: 需要查找的分隔符字节
     - `buf`: 存储读取结果的可变缓冲区
     - `read`: 记录本次读取操作已追加到缓冲区的字节数
     - `_pin`: 通过 `PhantomPinned` 确保 Future 不可移动（Unpin）
   - **特性**：
     - 使用 `pin_project_lite` 宏实现 Pin 语义，支持异步操作
     - 实现 `Future` trait，返回读取的字节数或错误

2. **`read_until` 工厂函数**
   - 创建 `ReadUntil` 实例，初始化参数并设置初始状态
   - 需要 `reader` 和 `buf` 是 `Unpin` 类型以确保兼容性

3. **`read_until_internal` 内部方法**
   - 核心逻辑循环：
     1. 调用 `poll_fill_buf` 获取可读缓冲区
     2. 使用 `memchr` 库高效查找分隔符位置
     3. 将数据追加到目标缓冲区，标记已读取字节数
     4. 根据是否找到分隔符或缓冲区耗尽决定是否终止
   - 处理异步轮询，通过 `Poll` 返回进度或结果

4. **Future 实现**
   - 通过 `poll` 方法委托给 `read_until_internal` 执行实际操作
   - 确保异步上下文（`Context`）正确传递

#### 工作流程
1. 调用 `read_until` 创建 Future 实例
2. 在异步执行时，`poll` 方法触发内部循环：
   - 填充缓冲区（`poll_fill_buf`）
   - 查找分隔符位置（`memchr`）
   - 更新缓冲区和状态
3. 当找到分隔符或缓冲区耗尽时返回结果

#### 项目中的角色