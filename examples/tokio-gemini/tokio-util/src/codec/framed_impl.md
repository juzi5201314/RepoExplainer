这个文件定义了 `FramedImpl` 结构体，它实现了 `Stream` 和 `Sink` trait，用于在异步 I/O 对象上进行编解码操作。它使用 `Decoder` 和 `Encoder` trait 来处理数据的编码和解码，从而将原始的字节流转换为有意义的帧。

**关键组件：**

*   **`FramedImpl<T, U, State>`**: 这是核心结构体，它封装了底层的 I/O 对象 (`T`)、编解码器 (`U`) 和状态 (`State`)。
    *   `T`:  实现了 `AsyncRead` 和 `AsyncWrite` trait 的类型，代表底层的 I/O 对象，例如网络连接或文件。
    *   `U`: 实现了 `Decoder` 和 `Encoder` trait 的类型，负责将字节流转换为帧，以及将帧转换为字节流。
    *   `State`:  用于跟踪读写操作的状态，包含 `ReadFrame` 和 `WriteFrame`。
*   **`ReadFrame`**:  用于管理读取操作的状态和缓冲区。
    *   `eof`:  表示是否已到达输入流的结尾。
    *   `is_readable`:  表示缓冲区中是否有可供解码的数据。
    *   `buffer`:  用于存储从底层 I/O 对象读取的字节的 `BytesMut` 缓冲区。
    *   `has_errored`:  表示是否发生了错误。
*   **`WriteFrame`**:  用于管理写入操作的状态和缓冲区。
    *   `buffer`:  用于存储要写入到底层 I/O 对象的字节的 `BytesMut` 缓冲区。
    *   `backpressure_boundary`:  用于控制背压的边界值。
*   **`RWFrames`**:  包含 `ReadFrame` 和 `WriteFrame`，用于同时管理读写状态。
*   **`INITIAL_CAPACITY`**:  定义了缓冲区初始容量的常量。
*   **`Stream` 实现**:  `FramedImpl` 实现了 `Stream` trait，允许从底层 I/O 对象读取帧。`poll_next` 方法负责从底层读取数据，使用 `Decoder` 解码数据，并返回解码后的帧。它维护一个状态机来处理不同的读取状态，例如读取中、解码中、EOF 等。
*   **`Sink` 实现**:  `FramedImpl` 实现了 `Sink` trait，允许将帧写入到底层 I/O 对象。`poll_ready` 方法检查是否可以发送数据，`start_send` 方法将帧编码为字节并放入缓冲区，`poll_flush` 方法将缓冲区中的字节写入到底层 I/O 对象，`poll_close` 方法关闭 I/O 对象。

**与其他部分的关系：**

*   `FramedImpl` 是 `Framed` 结构体的内部实现细节。`Framed` 结构体是用户与编解码器交互的主要接口。
*   它使用了 `Decoder` 和 `Encoder` trait，这些 trait 定义了编解码器的接口。
*   它使用了 `tokio::io::AsyncRead` 和 `tokio::io::AsyncWrite` trait，这些 trait 定义了异步 I/O 的接口。
*   它使用了 `bytes::BytesMut` 来管理字节缓冲区。
*   它使用了 `futures_core::Stream` 和 `futures_sink::Sink` trait，这些 trait 定义了异步流和接收器的接口。
