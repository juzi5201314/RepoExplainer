### TcpStream.rs 文件详解

#### 文件目的
该文件实现了 Tokio 异步运行时中的 TCP 连接核心结构 `TcpStream`，提供非阻塞的 TCP 网络通信能力。它封装了底层的 `mio::net::TcpStream`，并通过异步方法支持 Tokio 的事件驱动模型。

---

#### 核心组件与功能

##### 1. **结构定义**
```rust
pub struct TcpStream {
    io: PollEvented<mio::net::TcpStream>,
}
```
- **`PollEvented`**：包装 `mio::net::TcpStream`，负责事件注册和就绪状态管理，通过 `mio` 库实现 I/O 多路复用。
- **`mio::net::TcpStream`**：底层的非阻塞 TCP 连接，由 `mio` 库提供。

---

##### 2. **核心方法**

###### **连接管理**
- **`connect`**：异步连接远程地址，支持多地址尝试：
  ```rust
  pub async fn connect<A: ToSocketAddrs>(addr: A) -> io::Result<TcpStream> { ... }
  ```
  - 自动尝试所有解析出的地址，返回首个成功连接的实例。
  - 内部调用 `connect_addr` 和 `connect_mio` 完成实际连接和就绪状态检查。

- **`from_std`/`into_std`**：与标准库 `TcpStream` 互转：
  ```rust
  pub fn from_std(stream: std::net::TcpStream) -> io::Result<TcpStream> { ... }
  pub fn into_std(self) -> io::Result<std::net::TcpStream> { ... }
  ```
  - `from_std` 要求传入的 `TcpStream` 已设置为非阻塞模式。
  - `into_std` 将 Tokio 的 `TcpStream` 转换回标准库类型，保留非阻塞模式。

---

###### **I/O 操作**
- **读写方法**：
  ```rust
  pub fn try_read(&self, buf: &mut [u8]) -> io::Result<usize> { ... }
  pub fn try_write(&self, buf: &[u8]) -> io::Result<usize> { ... }
  ```
  - 非阻塞尝试读写，失败时返回 `WouldBlock`。
  - 通过 `poll_read_ready`/`poll_write_ready` 检查就绪状态。

- **异步就绪检查**：
  ```rust
  pub async fn ready(&self, interest: Interest) -> io::Result<Ready> { ... }
  pub async fn readable(&self) -> io::Result<()> { ... }
  pub async fn writable(&self) -> io::Result<()> { ... }
  ```
  - 等待指定事件（如可读、可写），支持并发读写操作。

---

###### **TCP 特性配置**
- **`nodelay`/`set_nodelay`**：控制 Nagle 算法：
  ```rust
  pub fn set_nodelay(&self, nodelay: bool) -> io::Result<()> { ... }
  ```
  - `nodelay = true` 禁用 Nagle，立即发送数据包。

- **`ttl`/`set_ttl`**：设置 IP 数据包生存时间：
  ```rust
  pub fn set_ttl(&self, ttl: u32) -> io::Result<()> { ... }
  ```

---

##### 3. **拆分读写半连接**
```rust
pub fn split<'a>(&'a mut self) -> (ReadHalf<'a>, WriteHalf<'a>) { ... }
pub fn into_split(self) -> (OwnedReadHalf, OwnedWriteHalf) { ... }
```
- **`split`**：借用方式拆分，允许并发读写但不能跨任务移动。
- **`into_split`**：所有权拆分，通过 `Arc` 包装实现跨任务安全，但需堆分配。

---

##### 4. **异步 trait 实现**
```rust
impl AsyncRead for TcpStream { ... }
impl AsyncWrite for TcpStream { ... }
```
- 实现 `AsyncRead` 和 `AsyncWrite` trait，支持 `read`、`write` 等异步扩展方法。

---

#### 项目中的角色