# 文件说明：`tokio/src/fs/hard_link.rs`

## **目的**  
该文件实现了 Tokio 异步运行时中的硬链接创建功能，提供了一个异步版本的 `std::fs::hard_link`。它允许开发者在异步环境中安全地创建文件硬链接，而无需阻塞主线程。

---

## **关键组件**

### **1. 异步化机制 (`asyncify`)**  
- 通过 `asyncify` 函数将标准库的同步函数 `std::fs::hard_link` 封装为异步操作。  
- `asyncify` 内部可能通过线程池或异步 I/O 机制执行阻塞操作，确保 Tokio 的非阻塞特性。

### **2. 函数定义**  
```rust
pub async fn hard_link(
    original: impl AsRef<Path>,
    link: impl AsRef<Path>
) -> io::Result<()> { ... }
```  
- **参数**：  
  - `original`: 需要被链接的原始文件路径。  
  - `link`: 新创建的硬链接路径。  
- **返回值**：`io::Result<()>`，包含可能的 I/O 错误（如路径无效、权限不足等）。  

### **3. 平台适配**  
- 在 Unix 系统上通过 `link` 系统调用实现。  
- 在 Windows 系统上通过 `CreateHardLink` API 实现。  
- 行为与标准库保持一致，但未来可能根据 Rust 官方调整。

### **4. 错误处理**  
- 若原始文件不存在、非文件类型或路径跨文件系统，将返回错误。  
- 其他标准 I/O 错误（如权限问题）也会被正确传递。

### **5. 示例用法**  
```rust
#[tokio::main]
async fn main() -> std::io::Result<()> {
    fs::hard_link("a.txt", "b.txt").await?; // 异步创建硬链接
    Ok(())
}
```

---

## **项目中的角色**  