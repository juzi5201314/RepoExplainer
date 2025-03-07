这个文件定义了 `AsyncFd` 结构体，它将一个 Unix 文件描述符与 Tokio 运行时关联起来，允许轮询其就绪状态。`AsyncFd` 封装了一个实现了 `AsRawFd` trait 的 IO 对象，例如网络套接字或管道。

**主要组件：**

*   **`AsyncFd<T: AsRawFd>`**:
    *   `registration`:  `Registration` 结构体，用于向 Tokio 运行时注册文件描述符，并接收就绪事件。
    *   `inner: Option<T>`:  封装的 IO 对象。`Option` 用于在 `drop` 和 `into_inner` 方法中处理所有权。
*   **`AsyncFdReadyGuard<'a, T: AsRawFd>`**:
    *   `async_fd: &'a AsyncFd<T>`:  对 `AsyncFd` 的引用。
    *   `event: Option<ReadyEvent>`:  表示一个尚未确认的 IO 就绪事件。
*   **`AsyncFdReadyMutGuard<'a, T: AsRawFd>`**:
    *   `async_fd: &'a mut AsyncFd<T>`:  对 `AsyncFd` 的可变引用。
    *   `event: Option<ReadyEvent>`:  表示一个尚未确认的 IO 就绪事件。
*   **`AsyncFdTryNewError<T>`**:
    *   `inner: T`:  创建 `AsyncFd` 失败时，原始的 IO 对象。
    *   `cause: io::Error`:  创建失败的原因。
*   **`TryIoError`**:
    *   一个简单的结构体，表示 `try_io` 方法返回的错误，表明 IO 资源返回了 `WouldBlock` 错误。

**关键方法：**

*   **`new(inner: T)` / `with_interest(inner: T, interest: Interest)`**:  创建 `AsyncFd`，并注册文件描述符到 Tokio 运行时。`new` 方法默认关注 `READABLE` 和 `WRITABLE` 事件，`with_interest` 允许指定关注的事件。
*   **`try_new(inner: T)` / `try_with_interest(inner: T, interest: Interest)`**:  创建 `AsyncFd` 的尝试版本，如果注册失败，返回 `AsyncFdTryNewError`。
*   **`get_ref(&self)` / `get_mut(&mut self)`**:  获取对内部 IO 对象的共享/可变引用。
*   **`into_inner(mut self)`**:  注销文件描述符，并返回内部 IO 对象，释放 `AsyncFd` 对其的所有权。
*   **`poll_read_ready(&self, cx: &mut Context<'_>)` / `poll_read_ready_mut(&mut self, cx: &mut Context<'_>)`**:  轮询文件描述符是否可读。如果不可读，则注册 waker。
*   **`poll_write_ready(&self, cx: &mut Context<'_>)` / `poll_write_ready_mut(&mut self, cx: &mut Context<'_>)`**:  轮询文件描述符是否可写。如果不可写，则注册 waker。
*   **`ready(&self, interest: Interest)` / `ready_mut(&mut self, interest: Interest)`**:  等待文件描述符变为就绪状态，返回 `AsyncFdReadyGuard` 或 `AsyncFdReadyMutGuard`。
*   **`readable(&self)` / `readable_mut(&mut self)`**:  等待文件描述符变为可读状态。
*   **`writable(&self)` / `writable_mut(&mut self)`**:  等待文件描述符变为可写状态。
*   **`async_io(&self, interest: Interest, mut f: impl FnMut(&T) -> io::Result<R>)` / `async_io_mut(&mut self, interest: Interest, mut f: impl FnMut(&mut T) -> io::Result<R>)`**:  在文件描述符就绪后，执行用户提供的 IO 操作。
*   **`try_io(&self, interest: Interest, f: impl FnOnce(&T) -> io::Result<R>)` / `try_io_mut(&mut self, interest: Interest, f: impl FnOnce(&mut T) -> io::Result<R>)`**:  尝试执行 IO 操作，如果文件描述符未就绪，则返回 `WouldBlock` 错误。
*   **`as_raw_fd(&self)`**:  返回文件描述符。
*   **`as_fd(&self)`**:  返回一个 `BorrowedFd`。
*   **`clear_ready(&mut self)`**:  清除就绪状态，通知 Tokio 重新等待就绪事件。
*   **`clear_ready_matching(&mut self, ready: Ready)`**:  清除特定的就绪状态。
*   **`retain_ready(&mut self)`**:  保留就绪状态。
*   **`ready(&self)`**:  获取与 guard 关联的 `Ready` 值。
*   **`try_io(&mut self, f: impl FnOnce(&'a AsyncFd<Inner>) -> io::Result<R>)`**:  在 `AsyncFdReadyGuard` 中执行 IO 操作，如果操作返回 `WouldBlock`，则清除就绪状态。

**作用：**
