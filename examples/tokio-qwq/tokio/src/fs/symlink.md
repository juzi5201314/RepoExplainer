# `tokio/src/fs/symlink.rs` 文件详解

## 文件目的
该文件实现了 Tokio 异步运行时中与符号链接操作相关的异步函数，提供非阻塞的文件系统交互能力。通过将标准库的同步文件操作转换为异步执行，避免阻塞事件循环。

---

## 核心组件

### 1. `symlink` 函数
```rust
pub async fn symlink(original: impl AsRef<Path>, link: impl AsRef<Path>) -> io::Result<()> { ... }
```
- **功能**：创建指向 `original` 的符号链接 `link`
- **参数**：
  - `original`：目标路径（可转换为 `Path`）
  - `link`：要创建的符号链接路径
- **实现机制**：
  - 使用 `asyncify` 将标准库的同步函数 `std::os::unix::fs::symlink` 封装为异步调用
  - 通过 `to_owned()` 复制路径对象确保所有权转移

---

### 2. 异步转换机制
```rust
asyncify(move || std::os::unix::fs::symlink(original, link)).await
```
- **`asyncify` 宏的作用**：
  - 将阻塞的系统调用提交到 Tokio 的线程池执行
  - 返回 `Future` 实现异步等待
  - 避免直接阻塞事件循环线程

---

### 3. 相关上下文中的其他函数
虽然代码片段未完整展示，但上下文显示该模块包含：
- `symlink_dir`：专门创建指向目录的符号链接
- `symlink_file`：专门创建指向文件的符号链接
- `read_link`：异步读取符号链接的目标路径
- `symlink_metadata`：获取符号链接的元数据
- `hard_link`：创建硬链接的异步实现

---

## 在项目中的角色
作为 Tokio 异步文件系统模块的重要组成部分，该文件通过异步化标准库的符号链接操作，为 Rust 异步程序提供：
1. 非阻塞的文件系统交互能力
2. 与 Tokio 事件循环的无缝集成
3. 安全的路径操作封装（通过 `Path` 处理）
4. Unix 系统的符号链接功能支持
