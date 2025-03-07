### 文件说明

#### 目的
该文件实现了 `tokio-stream` 库中的 `ReadDirStream` 结构体，将 Tokio 的异步目录读取功能 `tokio::fs::ReadDir` 封装为符合 `Stream` trait 的异步流。其核心目标是让用户能够通过流式接口（如 `StreamExt` 的扩展方法）更方便地处理异步目录遍历操作。

---

#### 关键组件

1. **结构体定义**
   ```rust
   pub struct ReadDirStream {
       inner: ReadDir,
   }
   ```
   - **`inner`**：包裹了 Tokio 的 `ReadDir` 对象，负责实际的异步目录读取操作。

2. **构造方法**
   ```rust
   pub fn new(read_dir: ReadDir) -> Self { ... }
   ```
   - 通过 `ReadDir` 实例创建 `ReadDirStream`，提供流式接口的入口。

3. **转换方法**
   ```rust
   pub fn into_inner(self) -> ReadDir { ... }
   ```
   - 将 `ReadDirStream` 转换回原始 `ReadDir` 对象，支持在必要时恢复底层操作。

4. **Stream Trait 实现**
   ```rust
   impl Stream for ReadDirStream {
       type Item = io::Result<DirEntry>;
       fn poll_next(...) -> Poll<Option<Self::Item>> { ... }
   }
   ```
   - **`poll_next` 方法**：通过 `self.inner.poll_next_entry(cx)` 调用 Tokio 的异步读取逻辑，并将返回值通过 `Result::transpose` 转换为符合 `Stream` trait 的格式（`Poll<Option<Result<...>>>` → `Poll<Result<Option<...>>>`）。
   - 支持通过 `next().await` 异步逐个获取目录条目。

5. **底层访问 trait**
   ```rust
   impl AsRef<ReadDir> for ReadDirStream { ... }
   impl AsMut<ReadDir> for ReadDirStream { ... }
   ```
   - 提供对内部 `ReadDir` 的不可变和可变引用，方便直接调用底层方法。

---

#### 使用示例
```rust
use tokio::fs::read_dir;
use tokio_stream::{StreamExt, wrappers::ReadDirStream};

#[tokio::main(flavor = "current_thread")]
async fn main() -> std::io::Result<()> {
    let dirs = read_dir(".").await?;
    let mut dirs = ReadDirStream::new(dirs);
    while let Some(dir) = dirs.next().await {
        let dir = dir?;
        println!("{}", dir.path().display());
    }
    Ok(())
}
```
- **功能**：异步遍历当前目录的所有条目，并打印路径。
- **关键点**：通过 `ReadDirStream` 将 `ReadDir` 转换为流，使用 `StreamExt` 的 `next()` 方法实现流式处理。

---

#### 项目中的角色