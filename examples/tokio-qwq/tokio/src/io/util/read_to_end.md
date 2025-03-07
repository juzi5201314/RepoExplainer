### 代码文件解释：`tokio/src/io/util/read_to_end.rs`

#### **文件目的**
该文件实现了 Tokio 异步运行时中的 `ReadToEnd` Future，用于将异步读取流（`AsyncRead`）中的所有数据读取到 `Vec<u8>` 中。它通过动态管理缓冲区扩展和异步轮询，高效完成全量读取操作。

---

#### **关键组件**

1. **`ReadToEnd` 结构体**
   - **定义**：使用 `pin_project_lite` 宏生成 Pin 安全的结构体，包含以下字段：
     - `reader`: 对异步读取源的可变引用。
     - `buf`: 使用 `VecWithInitialized` 包装的 `Vec<u8>`，管理缓冲区的初始化部分。
     - `read`: 已读取的字节数。
     - `_pin`: 通过 `PhantomPinned` 确保 Future 不可移动（`!Unpin`），兼容异步 trait 方法。
   - **作用**：作为 Future 的状态持有者，跟踪读取进度和缓冲区状态。

2. **`read_to_end` 函数**
   - **功能**：创建 `ReadToEnd` 实例，初始化缓冲区和计数器。
   - **参数**：接受 `AsyncRead` 类型的 `reader` 和目标 `Vec<u8>`。
   - **返回值**：返回 `ReadToEnd` Future，等待异步执行。

3. **`read_to_end_internal` 内部函数**
   - **逻辑**：循环调用 `poll_read_to_end` 直到完成或出错：
     - 若读取失败，返回错误。
     - 若读取到 EOF（返回 0），返回总读取字节数。
     - 否则累加读取字节数并继续循环。

4. **`poll_read_to_end` 核心读取函数**
   - **自适应缓冲区策略**：
     - **小缓冲区试探**：当主缓冲区满时，先用 32 字节临时缓冲区读取，判断是否到达 EOF，避免过度分配。
     - **动态扩容**：若数据量较大，则扩展主缓冲区容量，直接读取到主缓冲区。
   - **缓冲区管理**：
     - 使用 `ReadBuf` 安全地操作未初始化内存区域。
     - 通过 `VecWithInitialized` 确保缓冲区正确标记已初始化部分。

5. **Future 实现**
   - `ReadToEnd` 实现 `Future` trait，其 `poll` 方法调用 `read_to_end_internal`，驱动异步读取流程。

---

#### **技术细节**
- **Pin 安全性**：通过 `PhantomPinned` 确保结构体不可移动，符合异步 trait 的要求。
- **缓冲区优化**：采用自适应策略平衡内存分配效率，避免因固定扩容导致的性能损耗。
- **错误处理**：直接传递 I/O 错误，确保异步操作的透明性。

---

#### **项目中的角色**