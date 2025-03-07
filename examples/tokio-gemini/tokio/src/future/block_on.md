这个文件定义了一个名为 `block_on` 的函数，用于在当前线程上阻塞地运行一个异步 `Future`。它根据是否启用了 Tokio 运行时（通过 `cfg_rt!` 和 `cfg_not_rt!` 条件编译）来选择不同的实现。

**关键组件：**

*   **`cfg_rt!` 和 `cfg_not_rt!`：** 这些宏用于条件编译。如果启用了 Tokio 运行时（即 `cfg_rt!` 为真），则使用第一种实现；否则（`cfg_not_rt!` 为真），使用第二种实现。
*   **`block_on<F: Future>(f: F) -> F::Output`：** 这是 `block_on` 函数的定义。它接受一个实现了 `Future` trait 的类型 `F` 作为参数，并返回 `Future` 的输出类型 `F::Output`。
*   **运行时环境下的实现 (cfg_rt!)：**
    *   `crate::runtime::context::try_enter_blocking_region()`：尝试进入阻塞区域。如果当前线程已经在 Tokio 运行时中，则会失败，并抛出一个错误，防止在运行时内部阻塞线程。
    *   `e.block_on(f).unwrap()`：在阻塞区域内，使用运行时环境的 `block_on` 方法来阻塞地运行给定的 `Future`。`unwrap()` 用于处理可能发生的错误。
*   **非运行时环境下的实现 (cfg_not_rt!)：**
    *   `crate::runtime::park::CachedParkThread::new()`：创建一个 `CachedParkThread` 实例，用于管理线程的阻塞和唤醒。
    *   `park.block_on(f).unwrap()`：使用 `CachedParkThread` 的 `block_on` 方法来阻塞地运行给定的 `Future`。`unwrap()` 用于处理可能发生的错误。

**功能：**

`block_on` 函数的主要目的是允许在同步代码中运行异步 `Future`。它通过阻塞当前线程直到 `Future` 完成来达到这个目的。这在需要在同步上下文中等待异步操作完成时非常有用，例如在测试或某些特定的应用程序场景中。

**与项目的关系：**

这个文件是 Tokio 运行时库的一部分，提供了在不同环境下阻塞运行异步任务的能力。它允许用户在没有 Tokio 运行时的情况下，或者在 Tokio 运行时内部，阻塞地运行异步代码。
