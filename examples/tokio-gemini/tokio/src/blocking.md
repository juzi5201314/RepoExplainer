这个文件 `blocking.rs` 实现了 Tokio 运行时中用于在阻塞线程上执行任务的功能。它根据是否启用了 `rt` 特性标志来提供不同的实现。

**关键组件：**

*   **`cfg_rt!` 和 `cfg_not_rt!` 宏：** 这些宏用于条件编译。如果启用了 `rt` 特性，则使用 `cfg_rt!` 块中的代码；否则，使用 `cfg_not_rt!` 块中的代码。`rt` 特性启用时，表示 Tokio 运行时可用。
*   **`spawn_blocking` 函数：**
    *   **`cfg_rt!` 块：**  如果启用了 `rt` 特性，`spawn_blocking` 函数会使用 `crate::runtime::spawn_blocking` 函数，该函数负责在 Tokio 运行时管理的阻塞线程池中执行给定的闭包。
    *   **`cfg_not_rt!` 块：**  如果未启用 `rt` 特性，`spawn_blocking` 函数会 panic，并显示一条消息，说明需要启用 `rt` 特性。这表明在没有 Tokio 运行时的情况下，无法使用阻塞操作。
*   **`spawn_mandatory_blocking` 函数：**
    *   **`cfg_rt!` 块：**  如果启用了 `rt` 特性，并且启用了 `fs` 特性，`spawn_mandatory_blocking` 函数会使用 `crate::runtime::spawn_mandatory_blocking` 函数，该函数用于在阻塞线程上执行强制性的阻塞操作。
    *   **`cfg_not_rt!` 块：**  如果未启用 `rt` 特性，`spawn_mandatory_blocking` 函数会 panic，并显示一条消息，说明需要启用 `rt` 特性。
*   **`JoinHandle` 结构体：**
    *   **`cfg_rt!` 块：**  如果启用了 `rt` 特性，`JoinHandle` 结构体来自 `crate::task::JoinHandle`，表示一个异步任务的句柄，可以用于等待任务完成。
    *   **`cfg_not_rt!` 块：**  如果未启用 `rt` 特性，`JoinHandle` 结构体是一个简单的占位符，实现了 `Future` trait，但其 `poll` 方法会 `unreachable!`，表示在没有 Tokio 运行时的情况下，无法真正地等待任务完成。它还实现了 `Send` 和 `Sync` trait，以及 `Debug` trait。
*   **`assert_send_sync` 函数：**  在 `cfg_not_rt!` 块中，用于确保 `JoinHandle` 结构体是 `Send` 和 `Sync` 的。

**功能和作用：**

该文件定义了在 Tokio 运行时中执行阻塞操作的机制。它允许开发者将 CPU 密集型或 I/O 密集型操作从异步任务中分离出来，在阻塞线程上执行，从而避免阻塞 Tokio 的事件循环。通过 `spawn_blocking` 函数，开发者可以提交一个闭包，该闭包将在阻塞线程池中执行。`JoinHandle` 结构体允许开发者等待阻塞任务完成，并获取其结果。
