rust
use crate::codec::decoder::Decoder;
use crate::codec::encoder::Encoder;

use futures_core::Stream;
use tokio::io::{AsyncRead, AsyncWrite};

use bytes::BytesMut;
use futures_sink::Sink;
use pin_project_lite::pin_project;
use std::borrow::{Borrow, BorrowMut};
use std::io;
use std::pin::Pin;
use std::task::{ready, Context, Poll};

pin_project! {
    #[derive(Debug)]
    pub(crate) struct FramedImpl<T, U, State> {
        #[pin]
        pub(crate) inner: T,
        pub(crate) state: State,
        pub(crate) codec: U,
    }
}

const INITIAL_CAPACITY: usize = 8 * 1024;

#[derive(Debug)]
pub(crate) struct ReadFrame {
    pub(crate) eof: bool,
    pub(crate) is_readable: bool,
    pub(crate) buffer: BytesMut,
    pub(crate) has_errored: bool,
}

pub(crate) struct WriteFrame {
    pub(crate) buffer: BytesMut,
    pub(crate) backpressure_boundary: usize,
}

#[derive(Default)]
pub(crate) struct RWFrames {
    pub(crate) read: ReadFrame,
    pub(crate) write: WriteFrame,
}
```

---

### 代码文件解释

#### **文件目的**
该文件是 Tokio 框架中 `tokio-util` 库的 `codec` 模块的核心实现，用于提供基于帧（Frame）的异步 I/O 处理能力。它通过 `Decoder` 和 `Encoder`  trait 将底层的异步 I/O 流（如 TCP 连接）转换为更高层次的帧流，支持高效的读写操作。

---

#### **关键组件**

1. **`FramedImpl` 结构体**
   - **定义**：通过 `pin_project` 宏实现的可 Pin 的结构体，包含以下字段：
     - `inner`: 底层异步 I/O 对象（如 `AsyncRead` 或 `AsyncWrite`）。
     - `state`: 状态管理结构（`ReadFrame` 或 `WriteFrame`），用于缓冲和状态跟踪。
     - `codec`: 编解码器（实现 `Decoder` 和 `Encoder` trait）。
   - **作用**：作为 `Framed` 的内部实现，协调 I/O 操作、缓冲区管理及编解码逻辑。

2. **`ReadFrame` 和 `WriteFrame`**
   - **`ReadFrame`**:
     - `buffer`: 读缓冲区（`BytesMut`），存储接收到的字节。
     - `eof`: 标记是否已到达流结束。
     - `is_readable`: 标记缓冲区是否可读。
     - `has_errored`: 标记是否发生错误。
   - **`WriteFrame`**:
     - `buffer`: 写缓冲区，存储待发送的字节。
     - `backpressure_boundary`: 触发回压的阈值，超过此值时需主动刷新缓冲区。

3. **`RWFrames` 结构体**
   - 组合 `ReadFrame` 和 `WriteFrame`，通过 `Borrow` 和 `BorrowMut` trait 提供对读写状态的便捷访问。

---

#### **核心逻辑**

1. **`Stream` 实现（读操作）**
   - **触发条件**：当 `FramedImpl` 作为 `AsyncRead` 和 `Decoder` 使用时。
   - **流程**：
     1. **解码循环**：循环调用 `codec.decode()` 尝试从缓冲区中提取帧。
     2. **缓冲区不足时读取数据**：若缓冲区无法解码出完整帧，则通过 `poll_read_buf` 从底层 I/O 读取更多数据。
     3. **EOF 处理**：当检测到流结束时，调用 `codec.decode_eof()` 处理剩余数据。
     4. **状态管理**：通过 `is_readable`、`eof` 等标志跟踪读取状态，错误时标记 `has_errored` 并终止流。

2. **`Sink` 实现（写操作）**
   - **触发条件**：当 `FramedImpl` 作为 `AsyncWrite` 和 `Encoder` 使用时。
   - **流程**：
     1. **编码与缓冲**：调用 `codec.encode()` 将数据编码为字节并写入缓冲区。
     2. **回压控制**：当缓冲区大小超过 `backpressure_boundary` 时，触发 `poll_flush` 主动刷新。
     3. **刷新与关闭**：
        - `poll_flush`：将缓冲区数据写入底层 I/O。
        - `poll_close`：完成所有写操作并关闭连接。

---

#### **项目中的角色**
该文件是 Tokio 框架中 `Framed` 类型的核心实现，通过协调编解码器、缓冲区管理及异步 I/O 操作，为用户提供基于帧的流式处理能力，是构建协议解析和网络通信的关键组件。
