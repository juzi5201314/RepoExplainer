这个文件定义了 `UdpFramed` 结构体，它是一个将 `UdpSocket` 与 `Encoder` 和 `Decoder` 结合起来的结构体，用于处理基于 UDP 的帧。它实现了 `Stream` 和 `Sink` trait，允许以帧的形式读写 UDP 数据。

**关键组件：**

*   `UdpFramed<C, T>`：核心结构体，包含：
    *   `socket: T`：底层的 `UdpSocket`。
    *   `codec: C`：用于编码和解码帧的 `Codec`。
    *   `rd: BytesMut`：用于读取数据的缓冲区。
    *   `wr: BytesMut`：用于写入数据的缓冲区。
    *   `out_addr: SocketAddr`：发送数据的目标地址。
    *   `flushed: bool`：指示写入缓冲区是否已刷新。
    *   `is_readable: bool`：指示读取缓冲区中是否有可解码的数据。
    *   `current_addr: Option<SocketAddr>`：当前接收到的数据包的源地址。
*   `Stream` trait 实现：
    *   `poll_next`：从 `UdpSocket` 接收数据，使用 `Decoder` 解码成帧，并返回帧和源地址。
*   `Sink` trait 实现：
    *   `poll_ready`：检查是否可以发送数据。
    *   `start_send`：使用 `Encoder` 编码帧，并将目标地址和编码后的数据存储到缓冲区。
    *   `poll_flush`：将写入缓冲区的数据发送到 `UdpSocket`。
    *   `poll_close`：刷新并关闭连接。
*   `new` 方法：创建一个新的 `UdpFramed` 实例。
*   `get_ref` 和 `get_mut` 方法：分别获取对底层 `UdpSocket` 的只读和可变引用。
*   `codec` 和 `codec_mut` 方法：分别获取对底层 `Codec` 的只读和可变引用。
*   `read_buffer` 和 `read_buffer_mut` 方法：分别获取对读取缓冲区的只读和可变引用。
*   `into_inner` 方法：消耗 `Framed` 并返回底层的 `UdpSocket`。

**与项目的关系：**

这个文件提供了在基于 UDP 的网络通信中处理帧的抽象。它允许开发者使用 `Encoder` 和 `Decoder` 来定义自定义的帧格式，并使用 `Stream` 和 `Sink` 接口来方便地进行读写操作。这使得构建基于 UDP 的应用程序更加容易，例如，可以用于实现自定义的协议。
