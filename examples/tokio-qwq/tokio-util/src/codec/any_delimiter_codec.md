# 文件说明：`any_delimiter_codec.rs`

## **目的**  
该文件实现了 `AnyDelimiterCodec` 结构体，这是一个基于自定义分隔符的编码器和解码器。其核心功能是将字节流按指定分隔符拆分为数据块（解码），或在编码时用指定序列连接数据块。适用于需要灵活分隔符的网络协议或数据处理场景。

---

## **关键组件**

### **1. 结构体 `AnyDelimiterCodec`**
```rust
pub struct AnyDelimiterCodec {
    next_index: usize,          // 下一次搜索分隔符的起始位置（优化性能）
    max_length: usize,          // 单个数据块的最大长度（防止内存溢出）
    is_discarding: bool,        // 是否处于丢弃超长数据块的状态
    seek_delimiters: Vec<u8>,   // 用于解码的分隔符集合（如 `b",;\n\r"`）
    sequence_writer: Vec<u8>,   // 编码时使用的分隔序列（如 `b";"`）
}
```

#### **构造方法**
- **`new(seek_delimiters, sequence_writer)`**  
  创建无最大长度限制的实例，适用于信任源的数据。
- **`new_with_max_length(..., max_length)`**  
  设置最大长度限制，防止恶意输入导致内存占用过高（推荐用于不可信数据）。
- **`Default` 实现**  
  默认使用 `b",;\n\r"` 作为分隔符，`b","` 作为编码序列。

---

### **2. 解码逻辑 (`Decoder` trait 实现)**
```rust
fn decode(&mut self, buf: &mut BytesMut) -> Result<Option<Bytes>, ...> {
    loop {
        // 计算搜索范围（不超过 max_length+1）
        let read_to = cmp::min(self.max_length.saturating_add(1), buf.len());
        
        // 在缓冲区中查找第一个匹配的分隔符
        let offset = buf[self.next_index..read_to].iter().position(|b| ...);
        
        match (self.is_discarding, offset) {
            // 根据状态处理超长数据或正常分块
            // ...
        }
    }
}
```
- **核心逻辑**：  
  - 循环遍历缓冲区，定位第一个分隔符。  
  - 若数据块超过 `max_length`，触发错误并进入丢弃模式，直到遇到分隔符。  
  - 返回数据块（截断分隔符），或 `None` 表示缓冲区不足。

#### **`decode_eof` 方法**  
在流结束时返回剩余未处理的数据块。

---

### **3. 编码逻辑 (`Encoder` trait 实现)**
```rust
fn encode(&mut self, chunk: T, buf: &mut BytesMut) -> Result<(), ...> {
    buf.put(chunk.as_bytes());    // 写入原始数据
    buf.put(self.sequence_writer.as_ref()); // 追加分隔序列
    Ok(())
}
```
将数据块与预设序列拼接，形成最终的编码字节流。

---

### **4. 错误类型 `AnyDelimiterCodecError`**
```rust
pub enum AnyDelimiterCodecError {
    MaxChunkLengthExceeded, // 数据块超出最大长度
    Io(io::Error),          // I/O 相关错误
}
```
提供清晰的错误分类，便于上层处理。

---

## **项目中的角色**  
该文件是 Tokio 编码器/解码器库的核心组件之一，用于实现基于分隔符的流式数据处理。它支持灵活的分隔符配置和安全的最大长度限制，适用于网络协议解析（如 CSV、行分隔文本）或需要自定义分隔符的场景，确保高效且安全的数据传输与解析。

**该文件在项目中的角色：**  