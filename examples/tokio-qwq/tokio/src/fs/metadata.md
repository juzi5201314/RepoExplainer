# 文件说明：`tokio/src/fs/metadata.rs`

## **功能目的**
该文件实现了 Tokio 异步文件系统操作中的 `metadata` 函数，提供非阻塞的文件元数据查询功能。它是标准库 `std::fs::metadata` 的异步版本，允许在异步运行时中安全地获取文件/目录的元数据信息。

---

## **核心组件**
### **1. 函数定义**
```rust
pub async fn metadata(path: impl AsRef<Path>) -> io::Result<Metadata> { ... }
```
- **参数**：接受任何可转换为 `Path` 的类型（如 `&str`、`PathBuf` 等）
- **返回值**：`io::Result<Metadata>`，包含文件大小、权限、修改时间等元数据
- **异步机制**：通过 `asyncify` 宏将同步的 `std::fs::metadata` 封装为异步调用，避免阻塞事件循环

### **2. 实现原理**
- **符号链接处理**：会自动解析路径中的符号链接，获取最终目标文件的元数据（与 `std::fs::metadata` 行为一致）
- **平台适配**：
  - **Unix**：基于 `stat` 系统调用
  - **Windows**：基于 `GetFileAttributesEx` API
- **错误处理**：返回标准 I/O 错误（如权限不足、路径不存在等）

### **3. 关键技术**
- **`asyncify` 宏**：将阻塞的同步 I/O 操作包装为异步任务，通过线程池执行，确保 Tokio 事件循环不被阻塞
- **所有权管理**：通过 `path.as_ref().to_owned()` 确保路径参数安全传递到异步任务中

---

## **代码结构解析**
```rust
// 核心实现
pub async fn metadata(path: impl AsRef<Path>) -> io::Result<Metadata> {
    let path = path.as_ref().to_owned();
    asyncify(|| std::fs::metadata(path)).await
}
```
- **路径转换**：将输入路径转换为 `PathBuf` 所有权类型
- **异步封装**：通过 `asyncify` 将同步函数 `std::fs::metadata` 转换为异步执行

---

## **项目中的角色**
该文件是 Tokio 异步文件系统模块的核心组件之一，为开发者提供非阻塞的元数据查询能力，确保在异步编程场景中高效处理文件信息获取操作，是 Tokio 异步文件 API（如 `tokio::fs::metadata`）的实现基础。
