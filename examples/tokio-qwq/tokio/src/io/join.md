### 文件说明

#### 目的
该文件实现了 `Join` 结构体，用于将实现了 `AsyncRead` 和 `AsyncWrite` 的两个异步 I/O 对象合并为一个统一的句柄。通过组合读写能力，简化需要同时操作读写对象的场景（如网络连接的读写分离）。

#### 关键组件
1. **`join` 函数**
   - 创建 `Join` 实例，接受 `AsyncRead` 类型的 `reader` 和 `AsyncWrite` 类型的 `writer`。
   - 示例：`let joined_io = join(tcp_stream.reader(), tcp_stream.writer());`

2. **`Join` 结构体**
   - 通过 `pin_project_lite` 宏定义，包含被 `Pin` 标记的 `reader` 和 `writer` 字段。
   - 支持拆分 (`into_inner`) 和获取内部对象的引用/可变引用方法。
   - 提供 `reader_pin_mut` 和 `writer_pin_mut` 方法，返回 `Pin<&mut T>` 以安全操作被 `Pin` 的字段。

3. **Trait 实现**
   - **`AsyncRead`**: 将 `poll_read` 委托给内部 `reader`。
   - **`AsyncWrite`**: 将 `poll_write`、`poll_flush` 等方法委托给内部 `writer`。
   - **`AsyncBufRead`**: 若 `reader` 实现了 `AsyncBufRead`，则委托 `poll_fill_buf` 和 `consume`。

#### 工作原理
- **委托机制**：所有读操作通过 `Join` 的 `reader` 字段完成，写操作通过 `writer` 字段完成。
- **Pin 支持**：使用 `pin_project_lite` 确保结构体内字段在堆上保持稳定地址，满足异步操作的安全性要求。
- **统一接口**：将读写对象封装为单一结构体，允许通过 `Join` 实例同时操作两者，例如：
  ```rust
  joined_io.poll_read(...) // 调用 reader 的 poll_read
  joined_io.poll_write(...) // 调用 writer 的 poll_write
  ```

#### 项目中的角色
此文件为 Tokio 的异步 I/O 模块提供了将读写对象合并的功能，使开发者能够以统一的方式处理需要同时操作读写操作的场景（如 TCP 连接的读写分离），提升代码简洁性和可维护性。
