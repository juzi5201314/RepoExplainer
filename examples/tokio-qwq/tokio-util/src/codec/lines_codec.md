# `lines_codec.rs` 文件详解

## 文件目的
该文件实现了基于换行符（`\n`）的编解码器 `LinesCodec`，用于在异步 I/O 操作中对数据流进行行分割。它支持最大行长度限制，防止恶意输入导致内存溢出，并兼容不同操作系统的换行格式（自动处理 `\r\n`）。

---

## 核心组件

### 1. **结构体 `LinesCodec`**
```rust
pub struct LinesCodec {
    next_index: usize,
    max_length: usize,
    is_discarding: bool,
}
```
- **`next_index`**：记录下次搜索换行符的起始位置，优化重复搜索效率。
- **`max_length`**：行的最大允许长度（默认 `usize::MAX`，即无限制）。
- **`is_discarding`**：标志位，当检测到超长行时进入丢弃模式，直到遇到换行符。

#### 构造方法
- **`new()`**：创建无长度限制的编解码器。
- **`new_with_max_length()`**：设置最大行长度，推荐用于处理不可信输入。
- **`max_length()`**：获取当前最大行长度限制。

---

### 2. **辅助函数**
#### `utf8()`
将字节数组转换为 UTF-8 字符串，若转换失败返回 `InvalidData` 错误：
```rust
fn utf8(buf: &[u8]) -> Result<&str, io::Error> {
    str::from_utf8(buf).map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Unable to decode input as UTF8"))
}
```

#### `without_carriage_return()`
去除行尾的回车符 `\r`（兼容 Windows 换行格式 `\r\n`）：
```rust
fn without_carriage_return(s: &[u8]) -> &[u8] {
    if let Some(&b'\r') = s.last() {
        &s[..s.len() - 1]
    } else {
        s
    }
}
```

---

### 3. **Decoder 实现**
#### `decode()`
核心逻辑：循环搜索换行符 `\n`，根据状态处理数据：
- **正常模式 (`is_discarding = false`)**：
  - 找到 `\n`：提取行内容，去除 `\r` 并返回字符串。
  - 超过 `max_length`：触发错误并进入丢弃模式。
- **丢弃模式 (`is_discarding = true`)**：
  - 找到 `\n`：丢弃到当前位置，退出丢弃模式。
  - 未找到 `\n`：继续丢弃数据直到缓冲区为空。

#### `decode_eof()`
处理流结束时的剩余数据，确保返回未完成的行（若存在）。

---

### 4. **Encoder 实现**
将字符串编码为字节流，自动添加 `\n` 换行符：
```rust
fn encode(&mut self, line: T, buf: &mut BytesMut) -> Result<(), LinesCodecError> {
    buf.put(line.as_ref().as_bytes());
    buf.put_u8(b'\n');
    Ok(())
}
```

---

### 5. **错误类型 `LinesCodecError`**
```rust
pub enum LinesCodecError {
    MaxLineLengthExceeded,
    Io(io::Error),
}
```
- **`MaxLineLengthExceeded`**：行长度超过限制。
- **`Io`**：底层 I/O 错误（如编码解码失败）。

---

## 在项目中的角色