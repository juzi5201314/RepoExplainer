# 文件说明：compat.rs

## 文件目的
该文件为 Tokio 和 Futures 生态系统之间的异步 I/O 特性提供了兼容性层，允许 `tokio::io` 和 `futures-io` 的 `AsyncRead`/`AsyncWrite` 特性在两种不同异步运行时框架之间无缝转换。

---

## 核心组件

### 1. **Compat 结构体**
```rust
pin_project! {
    pub struct Compat<T> {
        #[pin]
        inner: T,
        seek_pos: Option<io::SeekFrom>,
    }
}
```
- **功能**：包装原始 I/O 类型，实现双向兼容。
- **字段**：
  - `inner`: 被包装的实际 I/O 对象（如文件句柄、网络流等）。
  - `seek_pos`: 用于跟踪 `AsyncSeek` 操作的当前位置（处理不同 trait 的 seek 同步）。

---

### 2. **扩展 trait**
通过四个扩展 trait 提供类型转换方法：
```rust
// 将 futures-io 转换为 Tokio
pub trait FuturesAsyncReadCompatExt: futures_io::AsyncRead {
    fn compat(self) -> Compat<Self>;
}

// 将 Tokio 转换为 futures-io
pub trait TokioAsyncReadCompatExt: tokio::io::AsyncRead {
    fn compat(self) -> Compat<Self>;
}

// 同样适用于 AsyncWrite 类型的 compat_write 方法
```
- **作用**：为不同 trait 的类型提供 `.compat()` 或 `.compat_write()` 方法，生成兼容包装器。

---

### 3. **核心 trait 实现**
通过为 `Compat<T>` 实现双向 trait，完成接口转换：
#### a. **读操作兼容**
```rust
// 将 futures-io 的 AsyncRead 转为 Tokio 的 AsyncRead
impl<T: futures_io::AsyncRead> tokio::io::AsyncRead for Compat<T> {
    fn poll_read(...) { ... }
}

// 反向转换
impl<T: tokio::io::AsyncRead> futures_io::AsyncRead for Compat<T> {
    fn poll_read(...) { ... }
}
```
- **关键处理**：在 `tokio` 的 `ReadBuf` 和 `futures` 的 `[u8]` 缓冲区之间进行数据格式转换。

#### b. **写操作兼容**
```rust
impl<T: futures_io::AsyncWrite> tokio::io::AsyncWrite for Compat<T> {
    fn poll_write(...) { ... }
    fn poll_shutdown(...) { ... } // 对应 futures 的 poll_close
}

impl<T: tokio::io::AsyncWrite> futures_io::AsyncWrite for Compat<T> {
    fn poll_close(...) { ... } // 对应 tokio 的 poll_shutdown
}
```
- **注意**：`shutdown` 和 `close` 方法的语义差异需要特殊映射。

#### c. **Seek 操作兼容**
```rust
impl<T: tokio::io::AsyncSeek> futures_io::AsyncSeek for Compat<T> {
    fn poll_seek(...) { ... }
}

impl<T: futures_io::AsyncSeek> tokio::io::AsyncSeek for Compat<T> {
    fn start_seek(...) { ... }
    fn poll_complete(...) { ... }
}
```
- **机制**：通过 `seek_pos` 字段跟踪操作状态，确保 seek 操作的原子性。

---

### 4. **平台相关扩展**
```rust
#[cfg(unix)]
impl<T: AsRawFd> AsRawFd for Compat<T> { ... }

#[cfg(windows)]
impl<T: AsRawHandle> AsRawHandle for Compat<T> { ... }
```
- **作用**：将底层文件描述符/句柄的访问权限代理给内部对象，确保系统级 I/O 操作的兼容性。

---

## 工作流程
1. **类型转换**：通过 `.compat()` 方法将原始类型包装为 `Compat<T>`。
2. **接口适配**：当调用 Tokio 或 Futures 的 trait 方法时，`Compat` 内部将请求转发给被包装对象，并处理格式差异。
3. **状态同步**：对于 seek 等复杂操作，通过 `seek_pos` 确保操作顺序和状态一致性。

---

## 项目中的角色