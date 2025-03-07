### 文件说明

#### 目的
该文件实现了 Tokio 异步 I/O 框架中 `AsyncReadExt::read_to_string` 方法的核心逻辑。其核心功能是将异步读取的字节流转换为 `String`，同时处理 UTF-8 校验和异步读取的底层实现。

---

#### 关键组件

1. **`ReadToString` 结构体**
   - **类型定义**：通过 `pin_project!` 宏定义的异步 future，实现了 `Future` trait。
   - **字段说明**：
     - `reader`: 异步读取源（实现了 `AsyncRead` trait）。
     - `output`: 最终存放结果的 `String` 引用。
     - `buf`: 使用 `VecWithInitialized` 管理的缓冲区，用于暂存读取的字节。
     - `read`: 已读取的字节数。
     - `_pin`: 确保 future 不可移动（`!Unpin`），兼容异步 trait 方法。

2. **`read_to_string` 函数**
   - **作用**：构造 `ReadToString` future 的工厂函数。
   - **逻辑**：
     - 将输入的 `String` 转换为字节向量（`Vec<u8>`）并清空原 `String`。
     - 初始化 `ReadToString` 实例，将缓冲区与读取器关联。

3. **`read_to_string_internal` 内部函数**
   - **流程**：
     1. 调用 `read_to_end_internal` 异步读取所有字节到缓冲区。
     2. 将缓冲区内容尝试转换为 `String`（校验 UTF-8）。
     3. 通过 `finish_string_read` 合并 I/O 结果与 UTF-8 校验结果，并更新输出 `String`。

4. **Future 实现**
   - **`poll` 方法**：
     - 通过 `Pin` 安全地访问内部字段。
     - 调用 `read_to_string_internal` 执行实际读取和转换逻辑。

---

#### 实现细节

- **缓冲区管理**：
  - 使用 `VecWithInitialized` 管理缓冲区，确保仅处理已初始化的字节区域。
  - 读取完成后，通过 `String::from_utf8` 校验 UTF-8 合法性。

- **异步协作**：
  - 通过 `ready!` 宏等待 `read_to_end_internal` 完成，实现异步非阻塞读取。
  - 利用 `Pin` 和 `project` 宏安全地解构 future 结构体。

- **错误处理**：
  - 合并 I/O 错误（如读取中断）和 UTF-8 校验错误，返回统一的 `io::Result`。

---

#### 项目中的角色
此文件为 Tokio 提供了异步读取流至 `String` 的核心实现，是 `AsyncReadExt` trait 的扩展方法 `read_to_string` 的底层 future，确保高效、安全地处理异步字节流到字符串的转换。

最后角色描述：  