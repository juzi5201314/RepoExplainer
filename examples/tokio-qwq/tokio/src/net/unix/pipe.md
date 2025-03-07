# 文件说明：Tokio Unix 管道实现

## 文件目的
该文件 `pipe.rs` 是 Tokio 异步运行时中 Unix 管道功能的核心实现，提供以下功能：
1. 匿名管道的创建
2. 命名管道（FIFO）的配置与打开
3. 异步读写端（`Sender` 和 `Receiver`）的实现
4. 与 Tokio 事件循环的集成

---

## 核心组件

### 1. 匿名管道创建函数
```rust
pub fn pipe() -> io::Result<(Sender, Receiver)>
```
- **功能**：创建双向匿名管道，返回写端(Sender)和读端(Receiver)
- **实现**：
  - 使用 `mio_pipe::new()` 创建底层管道
  - 通过 `PollEvented` 将文件描述符注册到 Tokio 事件循环
- **注意事项**：
  - 需在启用 I/O 的 Tokio 运行时中调用
  - 示例展示了如何与子进程通信

---

### 2. FIFO 配置选项 `OpenOptions`
```rust
pub struct OpenOptions
```
- **功能**：配置 FIFO 管道的打开方式
- **关键方法**：
  - `read_write(bool)`：设置读写模式（Linux 特有）
  - `unchecked(bool)`：跳过管道类型检查
  - `open_receiver()`/`open_sender()`：根据配置打开对应端
- **实现细节**：
  - 使用标准库 `OpenOptions` 基础功能
  - 自动设置非阻塞模式 (`O_NONBLOCK`)
  - 检查文件类型是否为管道（除非设置 `unchecked`）

---

### 3. 写端(Sender)实现
```rust
pub struct Sender
```
- **功能**：提供异步写入功能的管道写端
- **关键方法**：
  - `try_write()`：尝试立即写入（非阻塞）
  - `writable()`：等待可写就绪的 Future
  - `poll_write_ready()`：轮询检查写就绪状态
- **特性**：
  - 实现 `AsyncWrite` trait 支持异步写操作
  - 支持向量写入 (`try_write_vectored`)
  - 提供文件描述符转换方法 (`into_blocking_fd`)

---

### 4. 读端(Receiver)实现
```rust
pub struct Receiver
```
- **功能**：提供异步读取功能的管道读端
- **关键方法**：
  - `try_read()`：尝试立即读取（非阻塞）
  - `readable()`：等待可读就绪的 Future
  - `try_read_buf()`：缓冲区读取（需 `cfg_io_util`）
- **特性**：
  - 实现 `AsyncRead` trait 支持异步读操作
  - 向量读取 (`try_read_vectored`)
  - 支持 Linux 上的"弹性读取"（读写模式保持连接）

---

### 5. 底层辅助函数
```rust
fn is_pipe(fd: BorrowedFd<'_>) -> io::Result<bool>
```
- **功能**：检查文件描述符是否为管道
- **实现**：
  - 使用 `libc::fstat` 检查文件类型标志
  - 返回 `true` 当 `S_IFMT` 匹配 `S_IFIFO`

```rust
fn set_nonblocking(fd: BorrowedFd<'_>, current_flags: libc::c_int) -> io::Result<()>
```
- **功能**：设置文件描述符为非阻塞模式
- **实现**：
  - 使用 `fcntl` 的 `F_SETFL` 命令
  - 自动保留原有标志位

---

## 项目中的角色
该文件为 Tokio 提供了完整的 Unix 管道异步 I/O 支持，允许开发者：
- 创建匿名管道进行进程间通信
- 操作命名管道（FIFO）实现持久化通信
- 在异步上下文中安全地进行非阻塞读写操作
- 通过 Tokio 运行时的事件循环管理 I/O 事件
- 提供与标准库兼容的文件描述符接口
