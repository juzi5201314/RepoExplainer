### 代码文件解释

#### 目的
该文件定义了一个模拟异步读写（`AsyncRead` + `AsyncWrite`）的 `Mock` 类型，用于 Tokio 测试环境中的单元测试。通过预定义操作序列，开发者可以模拟网络或文件 I/O 的确定性行为，避免真实 I/O 的不可预测性。

#### 核心组件
1. **Mock 结构体**
   - 实现 `AsyncRead` 和 `AsyncWrite`，模拟真实 I/O 行为。
   - 内部通过 `Inner` 结构体管理操作队列和状态。
   - 提供 `Drop` 实现，确保所有预定义操作在测试结束时被正确执行。

2. **Builder 模式**
   - `Builder` 结构体通过链式调用定义 `Mock` 的行为序列：
     - `read/write`：指定预期的读写数据。
     - `read_error/write_error`：设置错误返回。
     - `wait`：插入延迟操作。
   - `build()` 方法生成配置好的 `Mock` 实例，`build_with_handle()` 还返回可动态添加操作的 `Handle`。

3. **Handle 手柄**
   - 允许在测试运行时动态追加操作（如 `read`、`write`、错误等）。
   - 通过无界通道（`mpsc::UnboundedSender`）与 `Mock` 内部通信。

4. **Action 枚举**
   - 定义可配置的操作类型：
     - `Read`/`Write`：指定数据缓冲区。
     - `Wait`：延迟时间。
     - `ReadError`/`WriteError`：错误信息（使用 `Arc` 支持克隆）。

5. **Inner 状态管理**
   - 使用 `VecDeque<Action>` 存储操作队列。
   - `poll_action()` 方法处理异步事件循环中的操作轮询。
   - `sleep` 和 `waiting` 字段管理延迟逻辑，通过 `tokio::time::Sleep` 实现异步等待。

#### 核心逻辑
- **读操作 (`poll_read`)**：
  - 根据预定义的 `Read` 操作填充目标缓冲区。
  - 若遇到 `ReadError`，返回错误。
  - 若当前无操作，注册等待唤醒。

- **写操作 (`poll_write`)**：
  - 验证写入的数据与预定义的 `Write` 缓冲区匹配。
  - 若匹配失败，触发断言错误（测试失败）。
  - 处理 `WriteError` 返回错误。

- **延迟 (`Wait`)**：
  - 使用 `tokio::time::sleep` 模拟异步等待，确保测试中的时间敏感逻辑可验证。

#### 项目中的角色