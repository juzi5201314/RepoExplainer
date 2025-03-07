### 文件目的
该文件定义了 Tokio 的 `AsyncReadExt` 扩展 trait，为实现了 `AsyncRead` 的类型提供丰富的异步读取操作实用方法。这些方法简化了常见的异步 IO 操作，如读取固定字节数、读取到容器、连接流、限制读取量等。

---

### 核心组件与功能

#### 1. **扩展 Trait 定义**
- **`AsyncReadExt` Trait**  
  继承自 `AsyncRead`，通过扩展方法为异步读取操作提供更高层次的抽象。所有 `AsyncRead` 类型（如 `File`, `TcpStream`）自动实现此 trait。

#### 2. **核心方法**
##### **基础读取方法**
- **`chain<R>(self, next: R)`**  
  将当前流与 `next` 流连接，先读完当前流再读后续流。
  ```rust
  let handle = file1.chain(file2); // 先读 file1，EOF 后读 file2
  ```

- **`read(&mut self, buf: &mut [u8])`**  
  异步读取数据到缓冲区，返回读取的字节数。支持取消安全（Cancel Safe）。

- **`read_buf<B>(&mut self, buf: &mut B)`**  
  使用 `BufMut` 类型的缓冲区读取数据，优化连续读取场景。

- **`read_exact(&mut self, buf: &mut [u8])`**  
  确保读取指定数量的字节，否则返回错误（如 EOF 提前）。

##### **数值类型读取**
通过宏 `read_impl!` 自动生成以下方法：
- **整数读取**  
  支持不同字节序（Big-Endian/LE）和大小（u8/i8 到 u128/i128）：
  ```rust
  let value = reader.read_u32_le().await?; // 小端序读取 32 位无符号整数
  ```

- **浮点数读取**  
  支持 `f32`/`f64` 的 Big-Endian 和 Little-Endian 格式。

##### **高级操作**
- **`read_to_end(&mut self, buf: &mut Vec<u8>)`**  
  将流中所有数据读取到 `Vec<u8>`，直到 EOF。

- **`read_to_string(&mut self, dst: &mut String)`**  
  将流中数据读取为 UTF-8 字符串，验证编码有效性。

- **`take(self, limit: u64)`**  
  创建限制读取量的适配器，最多读取 `limit` 字节后返回 EOF：
  ```rust
  let limited_reader = file.take(1024); // 最多读取 1KB
  ```

---

#### 3. **实现机制**
- **宏生成方法**  
  `read_impl!` 宏自动生成整数读取方法，减少重复代码，确保一致性。
- **适配器模式**  
  方法如 `Chain`、`Take` 返回适配器类型，封装复杂逻辑，保持接口简洁。
- **取消安全（Cancel Safety）**  
  标记方法是否支持在 `tokio::select!` 中安全取消，避免数据竞争。

---

#### 4. **使用示例**
```rust
use tokio::fs::File;
use tokio::io::{self, AsyncReadExt};

#[tokio::main]
async fn main() -> io::Result<()> {
    let mut file = File::open("data.bin").await?;
    
    // 读取固定字节数组
    let mut buffer = [0; 10];
    file.read_exact(&mut buffer).await?;
    
    // 读取到 Vec
    let mut data = Vec::new();
    file.read_to_end(&mut data).await?;
    
    // 读取整数
    let value = file.read_u16_le().await?;
    
    Ok(())
}
```

---

### 在项目中的角色