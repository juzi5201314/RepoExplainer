这段代码文件 `tokio/src/signal/unix.rs` 实现了在 Unix 系统上处理信号的机制，是 Tokio 库中信号处理模块的 Unix 特定实现。

**主要功能和组件：**

1.  **`SignalKind` 结构体：**
    *   表示要监听的特定类型的信号。
    *   提供了预定义的信号类型，如 `SIGINT` (中断), `SIGHUP` (挂断), `SIGTERM` (终止) 等。
    *   允许通过 `from_raw` 方法创建自定义信号类型。
    *   提供了将信号类型转换为原始信号值 (`c_int`) 的方法。

2.  **`Signal` 结构体：**
    *   是用于接收特定信号通知的监听器。
    *   通过 `signal` 函数创建，该函数会创建一个 `Signal` 实例，用于监听指定的信号类型。
    *   实现了 `recv` 和 `poll_recv` 方法，用于异步地接收信号通知。

3.  **`signal` 函数：**
    *   创建并返回一个 `Signal` 实例，用于监听指定的信号。
    *   在内部调用 `signal_with_handle` 函数。

4.  **`signal_with_handle` 函数：**
    *   启用信号处理。
    *   注册信号处理程序，如果尚未注册。
    *   返回一个 `watch::Receiver`，用于接收信号通知。

5.  **`action` 函数：**
    *   全局信号处理程序，当接收到注册的信号时被调用。
    *   记录事件，并通过写入管道唤醒驱动程序。

6.  **`OsStorage` 和 `OsExtraData` 结构体：**
    *   `OsStorage` 用于存储信号相关的信息。
    *   `OsExtraData` 包含用于信号处理的 Unix 域套接字对。

7.  **`SignalInfo` 结构体：**
    *   存储每个信号的事件信息，初始化状态等。

**代码流程：**

1.  调用 `signal(kind)` 函数创建一个 `Signal` 实例。
2.  `signal` 函数调用 `signal_with_handle` 函数。
3.  `signal_with_handle` 函数调用 `signal_enable` 函数。
4.  `signal_enable` 函数注册信号处理程序（如果尚未注册）。
5.  当接收到注册的信号时，`action` 函数被调用。
6.  `action` 函数记录事件，并通过写入管道唤醒驱动程序。
7.  `Signal` 实例的 `recv` 或 `poll_recv` 方法被调用，以接收信号通知。

**与其他模块的交互：**

*   与 `crate::runtime::scheduler` 交互，获取当前运行时句柄。
*   与 `crate::signal::registry` 交互，用于注册和管理信号处理程序。
*   与 `mio` 交互，用于创建 Unix 域套接字。
*   与 `signal_hook_registry` 交互，用于注册信号处理程序。

**总结：**

该文件实现了 Tokio 库在 Unix 系统上处理信号的核心逻辑，包括信号类型的定义、信号监听器的创建、信号处理程序的注册和信号通知的接收。
