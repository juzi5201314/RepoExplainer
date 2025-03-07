这个文件定义了 `FramedWrite` 结构体，它是一个将编码后的帧写入 `AsyncWrite` 的 `Sink`。它使用一个 `Encoder` 来将数据编码成字节，然后将这些字节写入底层的 `AsyncWrite`。

**主要组成部分：**

*   **`FramedWrite<T, E>` 结构体:**
    *   `T`:  实现了 `AsyncWrite` trait 的类型，代表了底层的 I/O 写入器。
    *   `E`:  实现了 `Encoder` trait 的类型，用于将数据编码成字节。
    *   `inner`:  一个 `FramedImpl` 结构体，封装了底层的 I/O 写入器、编码器和状态。`FramedImpl` 负责处理编码、缓冲和写入操作。
*   **`new()` 方法:**  创建一个新的 `FramedWrite` 实例，接收一个 `AsyncWrite` 实例和一个 `Encoder` 实例。
*   **`get_ref()`, `get_mut()`, `get_pin_mut()`, `into_inner()` 方法:**  提供了访问和获取底层 `AsyncWrite` 实例的方法。
*   **`encoder()`, `encoder_mut()`, `encoder_pin_mut()` 方法:**  提供了访问和获取底层 `Encoder` 实例的方法。
*   **`map_encoder()` 方法:**  允许将当前的编码器映射到另一个编码器，同时保留写入缓冲区。
*   **`write_buffer()`, `write_buffer_mut()` 方法:**  提供了访问和获取写入缓冲区的方法。
*   **`backpressure_boundary()`, `set_backpressure_boundary()` 方法:**  用于控制背压。
*   **`Sink` trait 的实现:**  实现了 `Sink` trait，允许将数据发送到 `FramedWrite`。`poll_ready`, `start_send`, `poll_flush`, 和 `poll_close` 方法被委托给 `FramedImpl` 处理。
*   **`Stream` trait 的实现:**  实现了 `Stream` trait，允许从底层的 `AsyncWrite` 中读取数据。
*   **`Debug` trait 的实现:**  提供了 `FramedWrite` 的调试输出。

**工作原理：**

1.  当调用 `Sink::start_send()` 方法时，数据会被传递给 `Encoder` 进行编码。
2.  编码后的字节被写入内部的缓冲区。
3.  当调用 `Sink::poll_flush()` 方法时，缓冲区中的数据会被写入底层的 `AsyncWrite`。
4.  `FramedWrite` 负责处理编码、缓冲和写入操作，确保数据被正确地编码和写入。

**与其他组件的关系：**

*   `Encoder`:  `FramedWrite` 使用 `Encoder` 将数据编码成字节。
*   `AsyncWrite`:  `FramedWrite` 将编码后的字节写入 `AsyncWrite`。
*   `FramedImpl`:  `FramedWrite` 内部使用 `FramedImpl` 来处理编码、缓冲和写入操作。
*   `futures_sink::Sink`:  `FramedWrite` 实现了 `Sink` trait，允许将数据发送到它。
*   `futures_core::Stream`: `FramedWrite` 实现了 `Stream` trait，允许从底层的 `AsyncWrite` 中读取数据。
