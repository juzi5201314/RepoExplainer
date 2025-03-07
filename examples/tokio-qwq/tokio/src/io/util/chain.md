### 文件说明：Chain.rs

#### 文件目的
该文件实现了 Tokio 异步 I/O 工具中的 `Chain` 结构体，用于将两个 `AsyncRead` 类型的流按顺序连接，形成一个连续的异步读取流。当第一个流读取完毕后，自动切换到第二个流继续读取。

---

#### 核心组件

1. **结构体定义**
   ```rust
   pub struct Chain<T, U> {
       #[pin] first: T,
       #[pin] second: U,
       done_first: bool,
   }
   ```
   - `first`：第一个异步读取源（类型 `T`）
   - `second`：第二个异步读取源（类型 `U`）
   - `done_first`：标记第一个流是否已完全读取完毕的布尔标志

2. **工厂方法**
   ```rust
   pub(super) fn chain<T, U>(first: T, second: U) -> Chain<T, U> 
   ```
   创建 `Chain` 实例，初始化时 `done_first` 默认为 `false`

3. **异步读取实现**
   ```rust
   impl<T, U> AsyncRead for Chain<T, U> {
       fn poll_read(...) {
           // 先尝试读取第一个流
           if !done_first {
               let rem = buf.remaining();
               ready!(first.poll_read(cx, buf))?;
               if buf.remaining() == rem { done_first = true }
           }
           // 第一个流读完后读取第二个流
           second.poll_read(cx, buf)
       }
   }
   ```
   - 优先读取第一个流，当读取到末尾（缓冲区未变化）时标记 `done_first`
   - 切换到第二个流继续读取

4. **缓冲读取扩展**
   ```rust
   impl<T, U> AsyncBufRead for Chain<T, U> {
       fn poll_fill_buf(...) {
           if !done_first {
               match first.poll_fill_buf()? {
                   [] => done_first = true,
                   buf => return Ok(buf),
               }
           }
           second.poll_fill_buf(cx)
       }
   }
   ```
   - 对 `AsyncBufRead` 类型的流提供缓冲读取支持
   - 自动处理缓冲区切换逻辑

5. **辅助方法**
   - `get_ref()`：获取内部流的不可变引用
   - `get_mut()`：获取内部流的可变引用（需谨慎使用）
   - `into_inner()`：析构后返回原始流

---

#### 关键特性
- **自动切换机制**：通过 `done_first` 标志自动管理流切换，无需用户手动处理
- **Pin 安全性**：使用 `pin_project_lite` 宏确保内部字段的 Pin 语义正确
- **无所有权转移**：通过 `Pin` 和投影实现零成本抽象，保持流的所有权在调用栈中

---

#### 项目中的角色