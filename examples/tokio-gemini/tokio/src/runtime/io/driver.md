这个文件定义了 Tokio 运行时中用于 I/O 操作的驱动程序。它基于 Mio 库，负责处理文件描述符的注册、注销、轮询和事件分发。

**关键组件：**

*   **`Driver` 结构体：**
    *   `signal_ready`: 一个布尔值，指示是否收到了信号 token 的事件。
    *   `events`:  `mio::Events` 实例，用于存储从操作系统接收到的事件。
    *   `poll`:  `mio::Poll` 实例，用于轮询 I/O 事件。
*   **`Handle` 结构体：**
    *   `registry`:  `mio::Registry` 实例，用于注册和注销 I/O 资源。
    *   `registrations`:  `RegistrationSet` 实例，用于跟踪所有注册的 I/O 资源。
    *   `synced`:  一个 `Mutex`，保护 `registration_set::Synced` 实例，用于同步注册信息。
    *   `waker`:  `mio::Waker` 实例，用于唤醒 I/O 驱动程序。仅在非 WASI 目标平台可用。
    *   `metrics`:  `IoDriverMetrics` 实例，用于收集 I/O 驱动程序的指标。
*   **`ReadyEvent` 结构体：** 封装了 I/O 就绪事件的信息，包括 tick、就绪状态和是否关闭。
*   **`Direction` 枚举：**  表示 I/O 操作的方向（读或写）。
*   **`Tick` 枚举：**  表示就绪状态的设置或清除。
*   **常量 `TOKEN_WAKEUP` 和 `TOKEN_SIGNAL`：**  用于标识唤醒和信号事件的 token。

**核心功能：**

*   **`Driver::new()`：**  创建一个新的 I/O 驱动程序实例，并返回一个 `Driver` 和一个 `Handle`。
*   **`Driver::park()` 和 `Driver::park_timeout()`：**  使 I/O 驱动程序进入休眠状态，等待 I/O 事件。
*   **`Driver::shutdown()`：**  关闭 I/O 驱动程序，并注销所有已注册的 I/O 资源。
*   **`Driver::turn()`：**  轮询 I/O 事件，处理就绪的 I/O 资源，并将事件分发给相应的处理程序。
*   **`Handle::unpark()`：**  唤醒 I/O 驱动程序。
*   **`Handle::add_source()`：**  将一个 I/O 资源注册到 I/O 驱动程序中。
*   **`Handle::deregister_source()`：**  从 I/O 驱动程序中注销一个 I/O 资源。
*   **`Handle::release_pending_registrations()`：** 释放挂起的注册。

**与其他组件的交互：**

*   与 `mio` 库交互，进行 I/O 事件的轮询和处理。
*   与 `crate::runtime::io` 模块交互，管理 I/O 资源的注册和注销。
*   与 `crate::runtime::driver` 模块交互，处理运行时驱动程序的控制。
*   使用 `IoDriverMetrics` 收集 I/O 驱动程序的指标。
