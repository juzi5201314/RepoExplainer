# 文件说明：`copy_buf.rs`

## 目的
该文件实现了 Tokio 异步 I/O 的 `copy_buf` 功能，用于高效地将异步缓冲读取器（`AsyncBufRead`）的内容异步复制到异步写入器（`AsyncWrite`）。通过直接利用读取器的内部缓冲区，避免了额外的内存分配，提升了性能。

---

## 关键组件

### 1. `CopyBuf` 结构体
```rust
struct CopyBuf<'a, R: ?Sized, W: ?Sized> {
    reader: &'a mut R,
    writer: &'a mut W,
    amt: u64,
}
```
- **功能**：作为异步 Future，负责管理复制过程的状态。
- **字段**：
  - `reader`: 异步缓冲读取器（实现 `AsyncBufRead`）
  - `writer`: 异步写入器（实现 `AsyncWrite`）
  - `amt`: 已复制的字节数统计

### 2. `copy_buf` 函数
```rust
pub async fn copy_buf<'a, R, W>(reader: &'a mut R, writer: &'a mut W) -> io::Result<u64> { ... }
```
- **功能**：创建并驱动 `CopyBuf` Future，返回最终复制的字节数。
- **特性**：
  - 参数需要实现 `AsyncBufRead` 和 `Unpin` trait。
  - 直接使用读取器的内部缓冲区，无需额外分配内存。

### 3. Future 实现（`poll` 方法）
```rust
impl<R, W> Future for CopyBuf<'_, R, W> { ... }
```
- **核心逻辑**：
  1. 循环读取缓冲区数据：通过 `poll_fill_buf` 获取读取器的缓冲区。
  2. 写入数据：通过 `poll_write` 异步写入缓冲区内容到目标。
  3. 状态更新：
     - `amt` 累加成功写入的字节数。
     - 调用 `consume` 标记已处理的缓冲区内容。
  4. 结束条件：
     - 读取到空缓冲区时返回成功。
     - 写入失败或写入 0 字节时返回错误。

---

## 工作原理
1. **缓冲区复用**：直接使用 `AsyncBufRead` 的内部缓冲区，避免额外拷贝。
2. **异步协作**：通过 `poll` 方法的轮询实现非阻塞操作，支持 Tokio 的异步运行时。
3. **错误处理**：任何 I/O 操作失败都会立即终止并返回错误。

---

## 项目中的角色
该文件为 Tokio 提供了高效的异步缓冲流复制功能，优化了 `AsyncBufRead` 类型（如 `BufReader`）的 I/O 性能，是 Tokio 异步 I/O 工具库的重要组成部分。
