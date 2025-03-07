# 文件说明：`canonicalize.rs`

## 功能概述
该文件实现了 Tokio 异步运行时的 `canonicalize` 函数，用于异步获取路径的规范绝对形式。这是标准库 `std::fs::canonicalize` 的异步版本，通过异步化处理避免阻塞事件循环。

## 关键组件

### 1. 函数定义
```rust
pub async fn canonicalize(path: impl AsRef<Path>) -> io::Result<PathBuf> { ... }
```
- **参数**：接受任何可转换为 `Path` 的类型
- **返回值**：`Result<PathBuf>`，成功时返回规范化的绝对路径
- **异步机制**：通过 `async/await` 语法实现异步执行

### 2. 核心实现
```rust
asyncify(move || std::fs::canonicalize(path)).await
```
- 使用 `asyncify` 宏将标准库的同步函数 `std::fs::canonicalize` 封装为异步操作
- `asyncify` 内部通过 Tokio 的线程池执行阻塞操作，确保不阻塞主线程

### 3. 平台差异处理
- **Unix系统**：基于 `realpath` 系统调用实现
- **Windows系统**：
  - 使用 `CreateFile` 和 `GetFinalPathNameByHandle` 组合
  - 自动转换为扩展长度路径（支持长路径但需注意兼容性）
  - 路径格式可能包含 `\\?\` 前缀

### 4. 错误处理
明确列出典型错误场景：
- 路径不存在
- 中间路径组件非目录
- 权限不足等标准 I/O 错误

## 示例用法
```rust
#[tokio::main]
async fn main() -> io::Result<()> {
    let path = fs::canonicalize("../a/../foo.txt").await?;
    // 使用规范化的绝对路径
    Ok(())
}
```

## 项目中的角色
该文件为 Tokio 异步文件系统模块提供路径规范化功能，通过异步化标准库操作，确保在异步运行时中高效安全地处理路径解析，同时兼容不同操作系统特性。
