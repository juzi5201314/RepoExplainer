rust
# unix_listener.rs 文件详解

## 文件目的
该文件实现了 `UnixListenerStream` 结构体，通过将 Tokio 的 `UnixListener` 封装为实现了 `Stream` 特性的类型，使得 Unix 域套接字监听器可以以流的方式异步处理连接请求。

## 关键组件

### 1. 结构体定义
```rust
pub struct UnixListenerStream {
    inner: UnixListener,
}
```
- **inner**：存储底层的 Tokio `UnixListener` 实例，负责实际的监听操作。

### 2. 构造方法
```rust
pub fn new(listener: UnixListener) -> Self {
    Self { inner: listener }
}
```
- 提供从 `UnixListener` 创建流实例的便捷方法。

### 3. 特性实现

#### Stream 特性实现
```rust
impl Stream for UnixListenerStream {
    type Item = io::Result<UnixStream>;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
    ) -> Poll<Option<io::Result<UnixStream>>> {
        match self.inner.poll_accept(cx) {
            Poll::Ready(Ok((stream, _))) => Poll::Ready(Some(Ok(stream))),
            Poll::Ready(Err(err)) => Poll::Ready(Some(Err(err))),
            Poll::Pending => Poll::Pending,
        }
    }
}
```
- **poll_next 方法**：通过调用 `UnixListener::poll_accept` 检查是否有新连接
- **返回值处理**：
  - 成功接受连接时返回 `Poll::Ready(Some(Ok(stream)))`
  - 出错时返回 `Poll::Ready(Some(Err(err)))`
  - 没有就绪连接时返回 `Poll::Pending`

#### AsRef/AsMut 特性
```rust
impl AsRef<UnixListener> for UnixListenerStream {
    fn as_ref(&self) -> &UnixListener { &self.inner }
}

impl AsMut<UnixListener> for UnixListenerStream {
    fn as_mut(&mut self) -> &mut UnixListener { &mut self.inner }
}
```
- 提供对底层 `UnixListener` 的安全引用访问，保持与原始类型的兼容性。

### 4. 示例用法
```rust
let listener = UnixListener::bind("/tmp/sock")?;
let mut incoming = UnixListenerStream::new(listener);

while let Some(stream) = incoming.next().await {
    let stream = stream?;
    println!("Accepted connection from: {:?}", stream.peer_addr()?);
}
```
- 展示如何将监听器转换为流，并通过 `.next().await` 异步处理连接

## 项目中的角色
该文件为 Tokio 生态系统提供了 Unix 域套接字监听器的流式处理能力，通过将 I/O 操作转换为流，使开发者能够以更简洁的异步迭代方式处理连接请求，是 tokio-stream crate 中 Unix 网络功能的重要实现组件。
