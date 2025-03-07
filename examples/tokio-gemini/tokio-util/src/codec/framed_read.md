这段代码定义了 `FramedRead` 结构体，它是一个 `Stream`，用于从实现了 `AsyncRead` 特质的底层 I/O 流中解码消息。它结合了 `AsyncRead` 和 `Decoder`，将原始字节流转换为结构化的消息流。

**关键组件：**

*   **`FramedRead<T, D>`**:  主结构体，它包装了一个 `AsyncRead` 类型的 `inner` 字段和一个 `Decoder` 类型的 `codec` 字段。`T` 代表底层 I/O 流的类型，`D` 代表解码器的类型。
*   **`FramedImpl<T, D, ReadFrame>`**:  内部结构体，处理实际的读取和解码逻辑。`ReadFrame` 存储了读取状态和缓冲区。
*   **`AsyncRead`**:  来自 `tokio::io`，表示异步读取数据的 trait。`FramedRead` 从实现了这个 trait 的类型（例如，TCP 连接、文件）读取数据。
*   **`Decoder`**:  来自 `crate::codec`，定义了如何将字节流解码成消息。`FramedRead` 使用这个 trait 将从 `AsyncRead` 读取的字节转换为应用程序可用的消息。
*   **`BytesMut`**:  来自 `bytes` crate，用于高效地存储和操作字节缓冲区。
*   **`Stream`**:  来自 `futures_core`，表示一个异步的数据流。`FramedRead` 实现了这个 trait，允许使用者通过 `poll_next` 方法异步地获取解码后的消息。
*   **`Sink`**:  来自 `futures_sink`，表示一个异步的写入器。`FramedRead` 实现了这个 trait，允许使用者将数据写入到底层的 `AsyncRead`。
*   **`pin_project`**:  一个宏，用于安全地对结构体中的字段进行 `Pin` 操作，这对于异步编程至关重要。

**功能：**

1.  **创建 `FramedRead`**:  提供了 `new` 和 `with_capacity` 方法来创建 `FramedRead` 实例。`new` 使用默认的缓冲区大小，而 `with_capacity` 允许指定初始缓冲区大小。
2.  **访问底层资源**:  提供了 `get_ref`, `get_mut`, `get_pin_mut`, `into_inner` 方法来访问和操作底层的 `AsyncRead` 和 `Decoder`。
3.  **访问解码器**:  提供了 `decoder`, `decoder_mut`, `decoder_pin_mut` 方法来访问和修改解码器。
4.  **访问缓冲区**:  提供了 `read_buffer`, `read_buffer_mut` 方法来访问和修改读取缓冲区。
5.  **解码数据**:  通过实现 `Stream` trait，`FramedRead` 持续从 `AsyncRead` 读取数据，使用 `Decoder` 解码数据，并将解码后的消息作为 `Stream` 的 `Item` 返回。
6.  **Sink 实现**: 通过实现 `Sink` trait，`FramedRead` 允许将数据写入到底层的 `AsyncRead`。
7.  **Debug 实现**: 提供了 `Debug` 实现，方便调试。

**与项目的关系：**

这个文件定义了 `FramedRead`，它是 `tokio-util` 库中用于处理基于帧的 I/O 的核心组件之一。它将原始的字节流转换为结构化的消息流，使得应用程序可以更方便地处理网络通信或其他基于帧的 I/O 操作。它与 `FramedImpl` 和 `Decoder` 协同工作，提供了高效且灵活的异步 I/O 框架。
