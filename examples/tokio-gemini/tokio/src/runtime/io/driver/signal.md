这个文件定义了 Tokio 运行时中处理信号相关的代码，主要涉及信号接收器的注册和信号就绪状态的维护。

**关键组件：**

*   **`Handle` 结构体:**  这个结构体代表了 Tokio 运行时中的句柄，用于管理 I/O 操作。
    *   `register_signal_receiver` 方法：该方法用于将一个 `mio::net::UnixStream` 注册到 `mio` 事件循环中，以便接收信号。它使用 `TOKEN_SIGNAL` 作为 token，并注册为可读事件 (`mio::Interest::READABLE`)。这使得当信号到达时，`mio` 能够通知 Tokio 运行时。

*   **`Driver` 结构体:**  这个结构体代表了 Tokio 运行时中的驱动程序，负责处理 I/O 事件。
    *   `signal_ready` 字段：一个布尔值，指示是否收到了信号。
    *   `consume_signal_ready` 方法：该方法用于消费信号就绪状态。它返回 `signal_ready` 的当前值，并将 `signal_ready` 重置为 `false`。这确保了信号只被处理一次。

**代码功能：**

1.  **注册信号接收器：** `Handle` 结构体的 `register_signal_receiver` 方法允许将一个 Unix 域套接字（`mio::net::UnixStream`）注册到 `mio` 事件循环中，以便接收信号。当信号到达时，`mio` 会触发一个可读事件。
2.  **处理信号就绪状态：** `Driver` 结构体的 `consume_signal_ready` 方法用于检查和消费信号就绪状态。当 Tokio 运行时收到信号事件时，它会设置 `signal_ready` 为 `true`。然后，`consume_signal_ready` 方法被调用来获取该状态，并将其重置为 `false`，从而避免重复处理信号。

**与其他部分的关联：**

*   `TOKEN_SIGNAL`：一个常量，用于标识信号事件。
*   `mio`：一个底层 I/O 多路复用库，Tokio 使用它来管理 I/O 事件。
*   `UnixStream`：用于接收信号的 Unix 域套接字。
*   `Driver` 和 `Handle`：Tokio 运行时中的核心组件，用于管理和处理 I/O 操作。
