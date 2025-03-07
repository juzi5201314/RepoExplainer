# 文件说明：`tokio/src/fs/create_dir.rs`

## 目的
该文件实现了 Tokio 异步文件系统模块中的 `create_dir` 函数，提供了一个异步版本的 `std::fs::create_dir`，用于在异步运行时（如 Tokio）中安全地创建单层目录。

## 关键组件

### 1. 函数定义
```rust
pub async fn create_dir(path: impl AsRef<Path>) -> io::Result<()> { ... }
```
- **参数**：接受任何可转换为 `Path` 的类型（如 `&str`、`String`、`PathBuf`）
- **返回值**：返回 `io::Result<()>`，包含可能的 I/O 错误
- **异步机制**：通过 `asyncify` 函数将同步的 `std::fs::create_dir` 封装为异步操作

### 2. 核心实现
```rust
asyncify(move || std::fs::create_dir(path)).await
```
- **`asyncify` 机制**：将阻塞的同步文件操作转移到后台线程执行，避免阻塞事件循环
- **路径处理**：通过 `path.as_ref().to_owned()` 确保路径的所有权转移

### 3. 功能特性
- **单层目录创建**：仅创建指定路径的最后一级目录
- **错误处理**：
  - 父目录不存在时返回错误（需使用 `create_dir_all` 处理多级目录）
  - 路径已存在或权限不足时返回对应错误
- **平台适配**：
  - Unix 系统调用 `mkdir`
  - Windows 系统调用 `CreateDirectory`

### 4. 相关函数对比
- `create_dir_all`：递归创建多级目录（见同目录的 `create_dir_all.rs`）
- `DirBuilder`：提供更复杂的目录创建选项（如权限设置）

## 项目中的角色