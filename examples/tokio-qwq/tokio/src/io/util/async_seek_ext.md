### 文件说明：`async_seek_ext.rs`

#### 文件目的
该文件定义了 `AsyncSeekExt` 扩展 trait，为实现了 `AsyncSeek` 的异步 I/O 类型提供实用方法。通过将传统的同步 `Seek` 操作转换为异步 future，使异步 I/O 操作能够更自然地与 `async/await` 语法配合使用。

#### 关键组件
1. **`AsyncSeekExt` Trait**
   - **继承要求**：必须实现 `AsyncSeek` trait。
   - **核心方法**：
     - `seek(pos: SeekFrom) -> Seek<'_, Self>`：创建一个 future，执行异步 seek 操作并返回新位置。
     - `rewind() -> Seek<'_, Self>`：快捷方法，等同于 `seek(SeekFrom::Start(0))`。
     - `stream_position() -> Seek<'_, Self>`：获取当前流位置，等同于 `seek(SeekFrom::Current(0))`。
   - **约束条件**：所有方法要求 `Self: Unpin`，因为 future 需要通过 `Pin` 进行安全移动。

2. **实现细节**
   - 通过 `seek` 函数（来自 `crate::io::seek` 模块）实现底层逻辑。
   - 方法返回的 `Seek` future 实现了 `Future<Output = io::Result<u64>>`，确保异步操作的兼容性。

#### 示例说明
- **Seek 操作示例**：
  ```rust
  let mut cursor = Cursor::new(b"abcdefg");
  cursor.seek(SeekFrom::Start(3)).await?;
  // 此时 cursor 位于第4个字节（'d'）
  ```
- **Rewind 示例**：
  ```rust
  file.rewind().await?; // 将文件指针重置到开头
  ```
- **获取当前位置**：
  ```rust
  let pos = cursor.stream_position().await?;
  ```

#### 项目中的角色
该文件为 Tokio 的异步 I/O 系统提供了 `AsyncSeek` 的扩展能力，通过封装异步 seek 操作为 future，简化了异步场景下的文件/流定位逻辑，是 Tokio 异步 I/O 工具链的重要组成部分。
