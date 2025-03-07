这个文件定义了 `Framed` 结构体，它将一个实现了 `AsyncRead` 和 `AsyncWrite` 特征的 I/O 对象与 `Encoder` 和 `Decoder` 特征结合起来，从而提供了一个统一的 `Stream` 和 `Sink` 接口，用于处理基于帧的数据。

**主要组成部分：**

*   **`Framed<T, U>` 结构体**:
    *   `inner`:  一个 `FramedImpl` 结构体的实例，它封装了底层的 I/O 对象 (`T`)、编解码器 (`U`) 和内部状态。`FramedImpl` 负责实际的读写操作和编解码逻辑。
*   **`new(inner: T, codec: U)` 函数**:
    *   创建一个 `Framed` 实例，使用给定的 I/O 对象和编解码器。
*   **`with_capacity(inner: T, codec: U, capacity: usize)` 函数**:
    *   创建一个 `Framed` 实例，并指定初始的读缓冲区容量。
*   **`from_parts(parts: FramedParts<T, U>)` 函数**:
    *   从 `FramedParts` 结构体创建一个 `Framed` 实例。这允许从之前的 `Framed` 实例中恢复状态，例如在拆分和重新组合 `Framed` 实例时使用。
*   **`get_ref(&self)`、`get_mut(&mut self)`、`get_pin_mut(self: Pin<&mut Self>)` 函数**:
    *   分别返回对底层 I/O 对象 (`T`) 的只读、可变和固定引用的方法。
*   **`codec()`、`codec_mut()`、`codec_pin_mut(self: Pin<&mut Self>)` 函数**:
    *   分别返回对编解码器 (`U`) 的只读、可变和固定引用的方法。
*   **`map_codec<C, F>(self, map: F)` 函数**:
    *   将编解码器 `U` 映射到 `C`，同时保留读写缓冲区。这允许在不改变 I/O 对象的情况下更改编解码器。
*   **`read_buffer()`、`read_buffer_mut()`、`write_buffer()`、`write_buffer_mut()` 函数**:
    *   分别返回对读写缓冲区的只读和可变引用的方法。
*   **`backpressure_boundary()`、`set_backpressure_boundary()` 函数**:
    *   用于设置和获取背压边界。
*   **`into_inner(self)` 函数**:
    *   消耗 `Framed` 实例，返回底层的 I/O 对象。
*   **`into_parts(self)` 函数**:
    *   消耗 `Framed` 实例，返回一个 `FramedParts` 结构体，其中包含底层的 I/O 对象、编解码器、读缓冲区和写缓冲区。
*   **`Stream` 和 `Sink` 的实现**:
    *   `Framed` 实现了 `Stream` 和 `Sink` 特征，允许它作为异步数据流的生产者和消费者。这些实现将操作委托给内部的 `FramedImpl`。
*   **`fmt::Debug` 的实现**:
    *   为 `Framed` 提供了 `Debug` 格式化输出，方便调试。
*   **`FramedParts<T, U>` 结构体**:
    *   一个结构体，用于保存 `Framed` 实例的各个部分，包括 I/O 对象、编解码器、读缓冲区和写缓冲区。这允许拆分和重新组合 `Framed` 实例。
*   **`FramedParts::new<I>(io: T, codec: U)` 函数**:
    *   创建一个新的 `FramedParts` 实例。

**工作原理：**

`Framed` 结构体将底层的 I/O 对象 (`T`) 包装起来，并使用 `Encoder` 和 `Decoder` 特征来处理数据的编码和解码。当从 `Framed` 读取数据时，它会使用 `Decoder` 从底层 I/O 对象读取原始字节，并将它们解码成帧。当向 `Framed` 写入数据时，它会使用 `Encoder` 将帧编码成字节，并将它们写入到底层 I/O 对象。

**与其他组件的关系：**

*   **`AsyncRead` 和 `AsyncWrite`**:  `Framed` 依赖于实现了这些特征的 I/O 对象，例如 `tokio::net::TcpStream`。
*   **`Encoder` 和 `Decoder`**:  `Framed` 使用这些特征来定义如何将数据编码成字节流以及如何将字节流解码成数据帧。
*   **`FramedImpl`**:  `Framed` 内部使用 `FramedImpl` 来处理实际的读写操作和编解码逻辑。
*   **`Stream` 和 `Sink`**:  `Framed` 实现了这两个特征，使其可以被用作异步数据流。
