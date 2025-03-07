### 文件说明

#### 目的
该文件实现了 Tokio 异步 IO 扩展中的 `read_exact` 功能，提供一个 Future 来确保从异步读取源（如网络流或文件）中读取**恰好填满指定缓冲区**的字节。若提前到达 EOF 则返回错误。

#### 核心组件
1. **`ReadExact` 结构体**
   - **字段**：
     - `reader`: 异步读取源（实现了 `AsyncRead` 和 `Unpin`）
     - `buf`: 使用 `ReadBuf` 管理缓冲区，支持零拷贝读取
     - `_pin`: 通过 `PhantomPinned` 确保 Future 不实现 `Unpin`，兼容异步 trait 方法
   - **作用**：作为 Future 的状态持有者，跟踪读取进度和缓冲区状态。

2. **`read_exact` 函数**
   - **功能**：创建 `ReadExact` Future 的工厂函数
   - **参数**：接受可变引用的读取源和目标缓冲区
   - **返回值**：初始化的 `ReadExact` 实例

3. **`poll` 方法实现**
   - **循环逻辑**：
     1. 检查缓冲区剩余空间（`remaining()`）
     2. 若剩余空间不为零，调用 `poll_read` 驱动读取
     3. 若读取后剩余空间未减少 → EOF 错误
     4. 若缓冲区填满 → 返回成功
   - **错误处理**：通过 `eof()` 函数生成 `UnexpectedEof` 错误

4. **`ReadBuf` 的作用**
   - 管理缓冲区的起始位置和剩余容量
   - 避免数据拷贝，直接操作用户提供的原始缓冲区

#### 工作流程
1. 调用 `AsyncReadExt::read_exact` 方法时，创建 `ReadExact` Future。
2. 在 Future 的 `poll` 方法中循环尝试读取：
   - 每次调用 `poll_read` 获取新数据
   - 更新 `ReadBuf` 的已读指针
   - 直到缓冲区填满或发生错误
3. 若读取过程中遇到 EOF 且未填满缓冲区 → 返回错误
4. 成功填满缓冲区 → 返回总字节数（`buf.capacity()`）

#### 项目中的角色