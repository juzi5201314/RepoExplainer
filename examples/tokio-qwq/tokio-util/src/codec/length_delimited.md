### 文件说明：`length_delimited.rs`

#### 目的
该文件实现了基于长度前缀的帧编码/解码器（`LengthDelimitedCodec`），用于在异步流中自动处理基于长度前缀的协议帧。它允许用户无需手动管理缓冲区或帧边界，即可直接操作完整的数据帧。

---

#### 核心组件

1. **`LengthDelimitedCodec` 结构体**
   - **功能**：负责帧的编码和解码。
   - **关键属性**：
     - `builder`: 配置参数（如最大帧长度、长度字段类型等）。
     - `state`: 解码状态（`Head` 或 `Data`），跟踪当前处理到帧的哪个部分。
   - **方法**：
     - `decode()`: 从字节流中解析完整帧，返回 `BytesMut`。
     - `encode()`: 将数据帧编码为带有长度前缀的字节流。
     - `new()`: 创建默认配置的实例（默认使用 `u32` 大端序，最大帧长度 8MB）。

2. **`Builder` 结构体**
   - **功能**：配置 `LengthDelimitedCodec` 的行为。
   - **关键配置项**：
     - `max_frame_length`: 允许的最大帧长度（超过则报错）。
     - `length_field_type`: 长度字段的类型（如 `u16`、`u32`）。
     - `length_field_offset`: 长度字段在帧头中的偏移量。
     - `length_adjustment`: 调整长度值（处理包含头部的长度或排除头部的情况）。
     - `num_skip`: 跳过的字节数（决定是否包含帧头到输出）。
   - **方法**：
     - `new()`: 创建默认配置的构建器。
     - `big_endian()`/`little_endian()`: 设置长度字段的字节序。
     - `new_read()`/`new_write()`/`new_framed()`: 根据配置生成对应的读/写适配器。

3. **错误处理**
   - `LengthDelimitedCodecError`: 当帧长度超过限制时抛出的错误。
   - 自动检查长度字段是否超出配置的最大值，并返回 `io::Error`。

---

#### 工作原理

1. **解码流程**
   - **步骤**：
     1. 读取帧头中的长度字段，计算实际数据长度（考虑 `length_adjustment`）。
     2. 跳过指定的字节数（`num_skip`），读取数据部分。
     3. 若数据不足，返回 `None` 并等待更多字节；若长度超限，返回错误。
   - **示例**：
     ```text
     +----------+--------------------------------+
     | len: u32 |          frame payload         |
     +----------+--------------------------------+
     ```
     默认配置下，长度字段为 `u32` 大端序，数据部分紧跟其后。

2. **编码流程**
   - **步骤**：
     1. 计算数据长度并应用调整（如需包含头部）。
     2. 将长度字段按配置的字节序写入字节流前缀。
     3. 追加原始数据。
   - **示例**：
     ```text
     +---- len: u32 ----+---- data ----+
     | \x00\x00\x00\x0b |  hello world |
     +------------------+--------------+
     ```

---

#### 配置灵活性

通过 `Builder` 可支持多种协议场景：
- **自定义长度字段类型**：如 `u16`、`usize`。
- **复杂帧头结构**：
  - 偏移量 (`length_field_offset`)：长度字段不在帧头起始位置。
  - 调整 (`length_adjustment`)：处理长度包含/排除头部的情况。
  - 跳过 (`num_skip`)：控制是否保留帧头到输出。

---

#### 在项目中的角色
该文件是 Tokio 生态中处理基于长度前缀协议的核心组件，为异步 I/O 提供了高性能、灵活的帧解码/编码能力，简化了协议实现的复杂度，使开发者能够专注于业务逻辑而非底层帧处理。
