# 文件说明：双向数据复制工具

## 文件目的
该文件提供了在两个异步流之间进行双向数据复制的功能，支持同时在两个方向上读写数据。当一方到达EOF时，会自动关闭另一方的写入通道，确保数据传输的完整性和可靠性。

## 核心组件

### 1. `TransferState` 枚举
```rust
enum TransferState {
    Running(CopyBuffer),
    ShuttingDown(u64),
    Done(u64),
}
```
- **Running**：数据传输进行中，使用`CopyBuffer`缓冲区持续读写。
- **ShuttingDown**：检测到EOF后，准备关闭写入通道。
- **Done**：传输完成，记录已传输的字节数。

### 2. `transfer_one_direction` 函数
```rust
fn transfer_one_direction(...) -> Poll<io::Result<u64>> { ... }
```
- **功能**：单向数据传输的核心逻辑，通过状态机管理传输流程：
  1. **Running**：调用`CopyBuffer.poll_copy`异步复制数据。
  2. **ShuttingDown**：调用`poll_shutdown`关闭写入端。
  3. **Done**：返回最终传输字节数。
- **实现**：通过无限循环轮询状态变化，直到传输完成。

### 3. 主函数 `copy_bidirectional` 和 `copy_bidirectional_with_sizes`
```rust
pub async fn copy_bidirectional<A, B>(...) { ... }
pub async fn copy_bidirectional_with_sizes<A, B>(...) { ... }
```
- **功能**：
  - `copy_bidirectional`：使用默认缓冲区大小（`DEFAULT_BUF_SIZE`）进行双向复制。
  - `copy_bidirectional_with_sizes`：允许自定义缓冲区大小。
- **实现**：
  1. 初始化两个`TransferState`实例分别处理`a→b`和`b→a`方向。
  2. 使用`poll_fn`创建未来，同时轮询两个方向的传输状态。
  3. 当两个方向均进入`Done`状态时，返回总传输字节数的元组。

### 4. `CopyBuffer` 缓冲区
- 从`super::copy`模块导入，负责在两个流之间高效缓冲和传输数据。
- 默认缓冲区大小由`DEFAULT_BUF_SIZE`定义（通常为8KB）。

## 工作流程
1. **初始化**：为两个方向分别创建缓冲区和状态机。
2. **并发传输**：
   - 同时启动`a→b`和`b→a`的异步复制。
   - 每个方向通过`TransferState`管理自身状态。
3. **EOF处理**：
   - 当某方向检测到EOF时，关闭对应写入端。
   - 另一方向继续传输直到完成。
4. **完成条件**：两个方向均完成传输后返回结果。

## 错误处理
- 若任一流发生I/O错误，立即终止并返回错误。
- 错误发生时可能有部分数据未传输完成。

## 项目中的角色
该文件是Tokio I/O工具集的核心组件之一，提供高效、可靠的双向异步数据传输功能，适用于网络代理、双向通信协议等场景。
```
