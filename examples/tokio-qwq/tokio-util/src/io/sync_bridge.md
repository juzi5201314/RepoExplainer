### 文件说明：SyncIoBridge 的实现与使用指南

#### 文件目的
`SyncIoBridge` 是 Tokio 生态中用于在同步上下文中使用异步 I/O 操作的桥梁。它允许将 `tokio::io::AsyncRead`/`AsyncWrite` 类型转换为标准库的 `std::io::Read`/`Write` 类型，从而兼容需要同步 I/O 的场景。尽管其存在必要性，但文件通过大量示例和警告强调了其潜在的性能问题，并推荐优先使用异步原生方案。

---

#### 核心组件
1. **结构定义**
   ```rust
   pub struct SyncIoBridge<T> {
       src: T,
       rt: tokio::runtime::Handle,
   }
   ```
   - `src`: 存储底层异步 I/O 对象（如 `AsyncRead` 或 `AsyncWrite`）
   - `rt`: Tokio 运行时句柄，用于在同步上下文中阻塞执行异步操作

2. **关键方法**
   - **构造方法**
     ```rust
     pub fn new(src: T) -> Self { ... }
     ```
     捕获当前运行时句柄，必须在异步上下文中调用。若需在外部线程使用，可通过 `new_with_handle` 手动指定运行时。

   - **阻塞执行**
     每个同步 trait 方法（如 `Read::read`）均通过 `rt.block_on` 调用对应的异步方法：
     ```rust
     fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
         self.rt.block_on(src.read(buf))
     }
     ```

3. **实现的同步 trait**
   - `Read`/`Write`: 基础读写操作
   - `BufRead`: 带缓冲的读取（如 `read_line`）
   - `Seek`: 文件指针定位
   - 扩展方法如 `is_write_vectored` 和 `shutdown` 提供对底层异步特性的访问

---

#### 使用场景与注意事项
1. **典型用途**
   - **与同步库交互**：当必须使用仅支持 `std::io` 的第三方库时，通过 `SyncIoBridge` 将 Tokio 异步流转换为同步流：
     ```rust
     let sync_reader = SyncIoBridge::new(async_reader);
     std::io::copy(&mut sync_reader, &mut file)?;
     ```

2. **性能警告**
   - **线程阻塞**：每次调用会阻塞当前线程，导致运行时无法处理其他任务。
   - **线程池耗尽**：过度使用可能导致 Tokio 线程池耗尽，推荐通过 `tokio::task::spawn_blocking` 将操作移至专用线程：
     ```rust
     let result = spawn_blocking(|| {
         std::io::copy(&mut sync_reader, &mut buffer)
     }).await??;
     ```

3. **最佳实践**
   - **数据处理**：优先在异步上下文中直接处理数据（如读取到内存后计算哈希）：
     ```rust
     async fn hash_contents(mut reader: impl AsyncRead + Unpin) {
         let mut data = Vec::new();
         reader.read_to_end(&mut data).await?;
         let hash = blake3::hash(&data);
     }
     ```
   - **流式处理**：对大文件采用增量处理，避免内存不足：
     ```rust
     async fn hash_stream(mut reader: impl AsyncRead + Unpin, mut hasher: Hasher) {
         let mut buffer = vec![0; 64 * 1024];
         loop {
             let len = reader.read(&mut buffer).await?;
             hasher.update(&buffer[..len]);
         }
     }
     ```

---

#### 在项目中的角色