这个文件定义了 `Registration` 结构体，它负责将 I/O 资源与驱动它的 reactor 实例关联起来。它提供了底层的 API，用于与 reactor 集成，并允许任务在就绪时接收通知。

**主要组件：**

*   **`Registration` 结构体：**
    *   `handle`:  指向关联的运行时句柄。
    *   `shared`:  对由驱动程序存储的状态的引用。
*   **`new_with_interest_and_handle` 方法：**
    *   将 I/O 资源注册到 reactor 中，并指定感兴趣的事件。
    *   返回 `Registration` 实例。
*   **`deregister` 方法：**
    *   从 reactor 中注销 I/O 资源。
    *   在 I/O 资源被释放之前必须调用此方法。
*   **`clear_readiness` 方法：**
    *   清除就绪状态。
*   **`poll_read_ready` 和 `poll_write_ready` 方法：**
    *   轮询 I/O 资源的读写就绪状态。
    *   需要调用者确保互斥性以保证正确性。
*   **`poll_read_io` 和 `poll_write_io` 方法：**
    *   轮询 I/O 操作，并在 I/O 就绪时执行给定的闭包。
*   **`poll_ready` 方法：**
    *   轮询 I/O 资源的指定方向的就绪流。
    *   如果提供了任务上下文，则在收到新事件时通知该任务。
*   **`poll_io` 方法：**
    *   循环调用 `poll_ready` 方法，直到 I/O 操作完成或发生错误。
*   **`try_io` 方法：**
    *   尝试执行 I/O 操作，如果资源未就绪，则返回 `WouldBlock` 错误。
*   **`readiness` 方法：**
    *   异步等待 I/O 资源的就绪状态。
*   **`async_io` 方法：**
    *   异步执行 I/O 操作。
*   **`handle` 方法：**
    *   返回运行时句柄。
*   **`Drop` 实现：**
    *   在 `Registration` 实例被释放时，清除 wakers 以打破循环引用。
*   **`gone` 函数：**
    *   创建一个表示运行时关闭的错误。

**功能：**

*   将 I/O 资源与 reactor 关联。
*   提供轮询 I/O 就绪状态的机制。
*   提供异步 I/O 操作的实现。
*   处理 I/O 资源的注册和注销。

**与其他组件的交互：**

*   与 `scheduler::Handle` 交互，获取 reactor 实例。
*   使用 `ScheduledIo` 存储驱动程序的状态。
*   使用 `mio` 库进行底层 I/O 操作。
