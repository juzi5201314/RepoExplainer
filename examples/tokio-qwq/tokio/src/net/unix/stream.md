### 文件说明：Tokio 的 Unix 域套接字异步实现

#### 文件目的
`src/net/unix/stream.rs` 是 Tokio 库中 Unix 域套接字（Unix Domain Socket）的异步实现核心文件。它提供了 `UnixStream` 结构体，用于在 Tokio 异步运行时中实现非阻塞的 Unix 域套接字通信，支持连接、读写、拆分读写半连接等功能。

---

#### 核心组件与功能

##### 1. **结构体定义**
```rust
pub struct UnixStream {
    io: PollEvented<mio::net::UnixStream>,
}
```
- **`PollEvented`**：来自 Tokio 的 I/O 事件轮询封装，负责将 Mio 的非阻塞套接字与 Tokio 的事件循环集成。
- **`mio::net::UnixStream`**：基于 Mio 库的底层 Unix 域套接字实现，提供非阻塞 I/O 能力。

---

##### 2. **关键方法**

###### **连接操作**
- **`connect`**：通过路径连接到 Unix 域套接字服务器：
  ```rust
  pub async fn connect<P>(path: P) -> io::Result<UnixStream>
  ```
  支持 Linux/Android 的抽象命名空间路径处理，通过 Mio 初始化连接并等待就绪状态。

- **`pair`**：创建无名的双向连接套接字对：
  ```rust
  pub fn pair() -> io::Result<(UnixStream, UnixStream)>
  ```

---

###### **读写操作**
- **就绪状态检查**：
  - **`ready(interest)`**：等待套接字变为可读或可写：
    ```rust
    pub async fn ready(&self, interest: Interest) -> io::Result<Ready>
    ```
  - **`readable()`/`writable()`**：便捷方法检查单一方向的就绪状态。

- **非阻塞读写**：
  - **`try_read`/`try_write`**：尝试立即读写数据，失败时返回 `WouldBlock`：
    ```rust
    pub fn try_read(&self, buf: &mut [u8]) -> io::Result<usize>
    ```

---

###### **拆分读写半连接**
- **`split`/`into_split`**：将套接字拆分为独立的读写半连接，支持并发操作：
  ```rust
  pub fn split<'a>(&'a mut self) -> (ReadHalf<'a>, WriteHalf<'a>)
  ```

---

###### **其他功能**
- **地址与错误处理**：
  - **`local_addr`/`peer_addr`**：获取本地/远程套接字地址。
  - **`take_error`**：获取套接字的错误状态。
  - **`shutdown`**：关闭读/写方向的连接。

- **与标准库互操作**：
  - **`from_std`/`into_std`**：在 Tokio 套接字与标准库 `std::os::unix::net::UnixStream` 之间转换。

---

##### 3. **异步 trait 实现**
- **`AsyncRead`/`AsyncWrite`**：实现 Tokio 的异步读写 trait，支持 `async/await` 风格的 I/O 操作：
  ```rust
  impl AsyncRead for UnixStream { ... }
  impl AsyncWrite for UnixStream { ... }
  ```

---

#### 在项目中的角色
该文件是 Tokio 异步 Unix 域套接字通信的核心实现，提供了安全高效的异步读写、连接管理、拆分操作等能力，是 Tokio 网络模块中 Unix 域套接字功能的基础，支持进程间通信（IPC）和高性能本地服务交互。
