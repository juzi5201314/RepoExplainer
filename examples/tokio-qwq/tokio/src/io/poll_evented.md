### 文件说明：`poll_evented.rs`

#### **文件目的**
`PollEvented` 是 Tokio 中用于将标准 I/O 资源（如 `TcpStream`、`File` 等）与事件循环（reactor）关联的核心结构。它通过 `mio` 库管理 I/O 资源的就绪事件，使得这些资源能够以异步方式（`AsyncRead`/`AsyncWrite`）被使用，同时避免阻塞线程。

---

#### **关键组件与功能**

1. **结构定义**
   ```rust
   pub(crate) struct PollEvented<E: Source> {
       io: Option<E>,
       registration: Registration,
   }
   ```
   - **`io`**: 存储实际的 I/O 资源（如 TCP 连接或文件句柄），使用 `Option` 以便在析构时安全释放。
   - **`registration`**: 通过 `Registration` 类型将 I/O 资源注册到事件循环，管理其读写兴趣（`Interest`）和就绪事件。

2. **创建与注册**
   - **`new` 和 `new_with_interest`**: 初始化 `PollEvented`，默认监听可读和可写事件。通过 `Registration` 将 I/O 资源注册到当前运行时的事件循环。
   - **`new_with_interest_and_handle`**: 允许自定义兴趣事件（如仅监听读事件），并指定运行时句柄。

3. **异步读写方法**
   - **`poll_read`**: 检查 I/O 资源是否可读，尝试读取数据。若读取部分数据或阻塞，则清除就绪状态以避免虚假通知。
     ```rust
     unsafe fn poll_read<'a>(&'a self, cx: &mut Context<'_>, buf: &mut ReadBuf<'_>) -> Poll<io::Result<>> 
     ```
   - **`poll_write`**: 类似 `poll_read`，但用于写操作。根据操作系统类型优化就绪状态的清除逻辑（如 epoll/kqueue 的边缘触发）。

4. **生命周期管理**
   - **`into_inner`**: 取消注册并返回原始 I/O 资源，常用于关闭连接。
   - **`Drop` 实现**: 确保析构时安全取消注册，避免资源泄漏。

5. **安全与并发**
   - **`Deref` 特性**: 允许直接访问内部 I/O 资源（如 `*poll_evented`）。
   - **并发限制**: 文档强调最多允许一个读任务和一个写任务同时操作，否则可能导致任务挂起或事件丢失。

---

#### **实现细节**
- **就绪事件处理**:
  - **`poll_read_ready`/`poll_write_ready`**: 检查当前就绪状态，若未就绪则挂起任务。
  - **`clear_readiness`**: 在 I/O 操作失败（如 `WouldBlock`）时手动清除就绪状态，确保下次操作时重新触发事件通知。

- **平台适配**:
  - 根据操作系统（如 Linux 的 epoll、macOS 的 kqueue）优化就绪状态的清除逻辑，避免不必要的轮询。

---

#### **在项目中的角色**