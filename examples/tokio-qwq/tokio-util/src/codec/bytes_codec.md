# `bytes_codec.rs` 文件详解

## **文件目的**
该文件实现了 Tokio 生态中一个基础的字节编码解码器 `BytesCodec`，用于在异步 I/O 操作中直接传输原始字节数据。它通过实现 `Decoder` 和 `Encoder` trait，提供无协议解析的原始字节流处理能力。

---

## **核心组件**

### **1. `BytesCodec` 结构体**
```rust
pub struct BytesCodec(());
```
- **特性**：空元组类型，实现了 `Copy`, `Clone`, `Default` 等基础 trait。
- **作用**：作为无状态的编码解码器实例，直接传递原始字节数据。
- **创建方法**：
  ```rust
  pub fn new() -> BytesCodec { BytesCodec(()) }
  ```

---

### **2. `Decoder` 实现**
```rust
impl Decoder for BytesCodec {
    type Item = BytesMut;
    type Error = io::Error;

    fn decode(&mut self, buf: &mut BytesMut) -> Result<Option<BytesMut>, io::Error> {
        if !buf.is_empty() {
            Ok(Some(buf.split_to(buf.len())))
        } else {
            Ok(None)
        }
    }
}
```
- **功能**：将缓冲区 `buf` 中的全部字节一次性提取为 `BytesMut` 对象。
- **行为**：
  - 当缓冲区非空时，返回整个缓冲区内容（通过 `split_to` 分割）。
  - 当缓冲区为空时，返回 `None`。
- **适用场景**：适用于无需分帧的原始字节流解码。

---

### **3. `Encoder` 实现**
#### **编码 `Bytes` 类型**
```rust
impl Encoder<Bytes> for BytesCodec {
    fn encode(&mut self, data: Bytes, buf: &mut BytesMut) -> Result<(), io::Error> {
        buf.reserve(data.len());
        buf.put(data);
        Ok(())
    }
}
```

#### **编码 `BytesMut` 类型**
```rust
impl Encoder<BytesMut> for BytesCodec {
    fn encode(&mut self, data: BytesMut, buf: &mut BytesMut) -> Result<(), io::Error> {
        buf.reserve(data.len());
        buf.put(data);
        Ok(())
    }
}
```
- **功能**：将输入数据直接追加到目标缓冲区 `buf` 中。
- **优化点**：
  - 使用 `reserve` 预留空间避免频繁扩容。
  - 通过 `put` 方法高效移动所有权，避免内存拷贝。
- **适用场景**：直接传输原始字节数据，不进行任何协议封装。

---

## **使用示例**
```rust
use tokio_util::codec::{FramedRead, BytesCodec};

let my_async_read = File::open("filename.txt").await?;
let my_stream_of_bytes = FramedRead::new(my_async_read, BytesCodec::new());
```
通过 `FramedRead` 结构体将 `AsyncRead` 对象包装为字节流，每次读取操作返回完整的缓冲区内容。

---

## **项目中的角色**