# 文件解释：`tokio-util/src/codec/mod.rs`

## **目的**
该文件是 Tokio 生态中 `tokio-util` 库的核心模块，提供将低层字节流（`AsyncRead`/`AsyncWrite`）转换为高层分帧协议（`Stream`/`Sink`）的适配器。其核心功能是通过定义编码器（`Encoder`）和解码器（`Decoder`）接口，实现字节流与应用层数据帧之间的转换，支持多种协议（如换行分隔、长度前缀等）。

---

## **关键组件**

### **1. 核心 trait**
- **`Decoder`**  
  定义如何将字节流解码为数据帧。  
  - **`decode` 方法**：根据缓冲区中的字节数据返回解码后的帧（`Option<Item>`）或错误。  
    - 若数据不足，返回 `Ok(None)`。  
    - 若数据足够，返回 `Ok(Some(frame))` 并更新缓冲区。  
    - 若数据无效，返回错误。  
  - 示例：`LinesCodec` 按换行符分割帧，`LengthDelimitedCodec` 按长度前缀解析帧。

- **`Encoder`**  
  定义如何将数据帧编码为字节流。  
  - **`encode` 方法**：将帧追加到缓冲区（`BytesMut`）中。  
  - 示例：`LinesCodec` 在字符串末尾添加换行符，`LengthDelimitedCodec` 在帧前添加长度前缀。

---

### **2. 核心结构**
- **`FramedRead`**  
  结合 `AsyncRead` 和 `Decoder`，将字节流转换为 `Stream<Item = Result<T>>`。  
  - 示例：从 TCP 流中按行读取数据。

- **`FramedWrite`**  
  结合 `AsyncWrite` 和 `Encoder`，将帧序列转换为 `Sink<T>`。  
  - 示例：将字符串按行编码后写入文件。

- **`Framed`**  
  全双工适配器，同时实现 `FramedRead` 和 `FramedWrite`，适用于双向通信（如 TCP 套接字）。

---

### **3. 协议实现**
模块提供了多种预定义的编码器/解码器：  
- **`LinesCodec`**：按换行符（`\n`）分隔帧。  
- **`LengthDelimitedCodec`**：按长度前缀分隔帧（如 Protobuf）。  
- **`AnyDelimiterCodec`**：自定义分隔符分隔帧。  
- **`BytesCodec`**：简单地将整个缓冲区作为一帧。

---

## **工作原理**
1. **编码流程**：  
   - 用户通过 `FramedWrite` 或 `Framed` 发送数据帧。  
   - `Encoder` 将帧编码为字节并追加到缓冲区。  
   - `FramedWrite` 定期将缓冲区内容写入 `AsyncWrite`（如 TCP 流）。

2. **解码流程**：  
   - `FramedRead` 或 `Framed` 从 `AsyncRead`（如 TCP 流）读取字节到缓冲区。  
   - `Decoder` 不断尝试从缓冲区解码完整帧，直到数据不足或完成解码。  
   - 解码后的帧通过 `Stream` 提供给用户。

---

## **项目中的角色**
该文件是 Tokio 生态中处理分帧协议的核心模块，为异步 I/O 提供高层协议支持，允许开发者通过简单适配器快速实现基于帧的通信（如行协议、长度前缀协议等），是构建网络应用和协议的关键组件。
