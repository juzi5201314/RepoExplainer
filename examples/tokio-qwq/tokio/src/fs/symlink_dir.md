# 文件说明：`tokio/src/fs/symlink_dir.rs`

## 功能概述  
该文件实现了 Tokio 异步文件系统操作中的 **创建目录符号链接** 功能。通过异步方式在 Windows 平台上创建目录软链接，使 `link` 路径指向 `original` 路径。

---

## 核心代码分析  

### 依赖与导入  
```rust
use crate::fs::asyncify;
use std::io;
use std::path::Path;
```
- `asyncify`：Tokio 内部工具函数，用于将阻塞的同步 I/O 操作转换为异步执行（通过线程池调度）。
- 标准库依赖：提供路径操作和 I/O 结果类型。

---

### `symlink_dir` 函数  
```rust
pub async fn symlink_dir(original: impl AsRef<Path>, link: impl AsRef<Path>) -> io::Result<()> {
    let original = original.as_ref().to_owned();
    let link = link.as_ref().to_owned();

    asyncify(move || std::os::windows::fs::symlink_dir(original, link)).await
}
```

#### 参数与返回值  
- **参数**：  
  - `original`：目标目录路径（被链接的原始路径）。  
  - `link`：要创建的符号链接路径。  
- **返回值**：`io::Result<()>`，表示操作是否成功。

#### 实现逻辑  
1. **路径转换**：  
   将传入的 `original` 和 `link` 转换为 `PathBuf` 所有权类型，确保闭包可以安全移动数据。  
2. **异步化调用**：  
   通过 `asyncify` 将同步函数 `std::os::windows::fs::symlink_dir` 封装为异步任务。  
   - `std::os::windows::fs::symlink_dir` 是 Rust 标准库中 Windows 平台的同步符号链接创建函数。  
   - `asyncify` 会将此操作提交到 Tokio 的线程池执行，避免阻塞事件循环。

---

## 项目中的角色  
该文件是 Tokio 异步文件系统模块的一部分，**为 Windows 平台提供非阻塞的目录符号链接创建功能**，确保在异步运行时中安全高效地执行 I/O 操作。

```  