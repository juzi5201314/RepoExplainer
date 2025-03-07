这个文件展示了如何将 Tokio 运行时与任何其他执行器结合使用。

**主要组成部分：**

1.  **`main` 函数：**
    *   使用 `oneshot::channel` 创建一个单次发送通道，用于在 Tokio 任务完成时进行信号通知。
    *   调用 `my_custom_runtime::spawn` 启动一个异步任务，该任务绑定一个 `TcpListener` 到一个随机端口，并打印监听地址。
    *   通过 `tx.send(())` 发送信号，表示任务已完成。
    *   使用 `futures::executor::block_on(rx)` 阻塞当前线程，直到接收到来自通道的信号，从而等待 Tokio 任务完成。

2.  **`my_custom_runtime` 模块：**
    *   **`spawn` 函数：**
        *   接收一个 `Future` 作为参数，并将其传递给内部的执行器进行执行。
    *   **`ThreadPool` 结构体：**
        *   包含一个 `futures::executor::ThreadPool` 用于执行任务。
        *   包含一个 `tokio::runtime::Runtime` 用于处理 Tokio 的 IO 和定时器。
    *   **`EXECUTOR` 静态变量：**
        *   使用 `once_cell::sync::Lazy` 确保只初始化一次。
        *   创建一个 Tokio 运行时，启用 IO 和定时器。
        *   创建一个 `futures::executor::ThreadPool`。
        *   将 Tokio 运行时和 `ThreadPool` 封装在 `ThreadPool` 结构体中。
    *   **`ThreadPool` 的 `spawn` 方法：**
        *   获取 Tokio 运行时的句柄。
        *   使用 `TokioContext::new` 包装传入的 `Future`，确保在轮询时进入 Tokio 上下文。
        *   使用 `inner.spawn_ok` 将包装后的 Future 提交给 `futures::executor::ThreadPool` 执行。

**工作原理：**

该示例创建了一个自定义的执行器，它将 Tokio 运行时嵌入其中。当调用 `my_custom_runtime::spawn` 时，它会将给定的 Future 包装在一个 `TokioContext` 中，确保在轮询时进入 Tokio 的上下文。然后，它使用 `futures::executor::ThreadPool` 来执行这个包装后的 Future。Tokio 运行时负责处理 IO 和定时器操作。这个例子展示了如何将 Tokio 与其他执行器结合使用，从而实现更灵活的异步编程。

**文件在项目中的作用：**
