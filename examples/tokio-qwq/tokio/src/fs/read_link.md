# 文件说明：tokio/src/fs/read_link.rs

## 文件目的
该文件实现了 Tokio 异步文件系统操作中的 `read_link` 函数，提供非阻塞的符号链接解析能力。作为标准库 `std::fs::read_link` 的异步版本，它允许在异步运行时中安全地读取符号链接的目标路径。

## 关键组件
### 核心函数
```rust
pub async fn read_link(path: impl AsRef<Path>) -> io::Result<PathBuf> {
    let path = path.as_ref().to_owned();
    asyncify(move || std::fs::read_link(path)).await
}
```
1. **参数处理**：通过 `path.as_ref().to_owned()` 将输入路径转换为 `PathBuf` 所有权，确保闭包可安全移动。
2. **异步化机制**：调用 `asyncify` 函数将同步的 `std::fs::read_link` 封装为异步任务。`asyncify` 会将阻塞操作提交到 Tokio 的任务线程池执行，避免阻塞事件循环线程。
3. **返回类型**：返回 `PathBuf` 类型的异步结果，符合 Tokio 异步流式编程范式。

### 依赖关系
- **`asyncify` 函数**：来自 `crate::fs::asyncify`，是 Tokio 内部用于将阻塞操作转换为异步任务的核心工具。
- **标准库依赖**：直接调用 `std::fs::read_link` 实现底层功能。

## 在项目中的角色