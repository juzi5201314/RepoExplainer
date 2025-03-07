# 文件说明：Tokio TCP 模块的 `mod.rs` 文件

## 文件目的
该文件是 Tokio 异步运行时中 TCP 网络模块的核心入口文件，负责组织和导出 TCP 相关的实用类型与功能。其核心目标是为异步 TCP 网络通信提供高效的读写分离、流处理以及监听器支持，同时遵循 Rust 的所有权和借用规则。

---

## 关键组件与功能

### 1. **子模块导出**
- **`listener`**：实现 TCP 监听器 (`TcpListener`)，用于异步监听传入连接。
- **`socket`**：通过 `cfg_not_wasi!` 宏条件编译，仅在非 WASI 环境中启用，提供底层 TCP 套接字 (`TcpSocket`) 的配置与绑定功能。
- **`stream`**：定义 TCP 流 (`TcpStream`)，用于异步读写数据。

### 2. **流的分离（Splitting）**
- **`split` 模块**：
  - 提供 `split` 函数，将 `TcpStream` 的可变引用拆分为 `ReadHalf` 和 `WriteHalf`，允许在不移动所有权的情况下并发读写。
  - 示例：`(ReadHalf<'_>, WriteHalf<'_>) = split(&mut stream)`。
- **`split_owned` 模块**：
  - 提供 `split_owned` 函数，将 `TcpStream` 所有权拆分为 `OwnedReadHalf` 和 `OwnedWriteHalf`，使读写部分可以独立传递到不同任务。
  - 异常 `ReuniteError`：当尝试合并无效的分离流时触发。

### 3. **类型导出**
- **`ReadHalf`/`WriteHalf`**：基于引用的读写半流，适用于短期借用场景。
- **`OwnedReadHalf`/`OwnedWriteHalf`**：基于所有权的半流，支持跨任务传递和长生命周期操作。
- **`TcpStream`**：通过 `pub(crate)` 导出，确保 Tokio 内部可访问，但对外部隐藏实现细节。

### 4. **条件编译与平台适配**
- **`cfg_not_wasi!`**：在 WebAssembly System Interface (WASI) 环境中禁用 `socket` 模块，因 WASI 不支持传统套接字操作。

---

## 在项目中的角色
该文件是 Tokio TCP 网络模块的核心组织者，通过模块化设计和类型分离，为异步 TCP 通信提供了灵活且安全的 API。它支持高效的读写并发、所有权管理，并适配不同运行时环境（如 WASI），是构建异步 TCP 服务器和客户端的基础组件。
