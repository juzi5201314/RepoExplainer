这个文件 `src/lib.rs` 实现了基于 Tokio 和 Futures 的测试工具。

**主要组成部分：**

*   **模块声明：**
    *   `io`: 包含用于模拟 I/O 操作的工具。
    *   `stream_mock`: 包含用于模拟流的工具。
    *   `macros`: 包含一些用于简化测试的宏。
    *   `task`: 包含用于处理任务的工具。
*   **`block_on` 函数：**
    *   这个函数是核心功能，它接受一个 `Future` 作为输入，并在当前线程上阻塞执行该 Future，直到它完成。
    *   它使用 `tokio::runtime::Builder` 创建一个单线程的 Tokio 运行时，并启用所有功能。
    *   然后，它使用 `rt.block_on(future)` 在运行时中阻塞执行给定的 Future。
*   **宏：**
    *   `assert_ready_eq!`：用于断言一个 Future 的 `poll` 方法返回 `Ready` 状态，并且结果与预期值相等。

**与其他部分的关联：**

*   该文件提供了测试 Tokio 和 Futures 代码的实用工具。
*   `block_on` 函数允许在测试环境中同步地运行异步代码。
*   `io` 和 `stream_mock` 模块提供了模拟 I/O 和流操作的能力，方便测试。
*   `task` 模块提供了用于处理任务的工具，例如 `spawn` 函数。
*   `macros` 模块提供了一些简化测试的宏，例如 `assert_ready_eq!`。

**总结：**
