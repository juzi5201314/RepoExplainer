这个文件定义了用于测试 Future 和 Stream 的辅助工具，特别是 `Spawn` 结构体，它提供了一个模拟的任务环境，允许在没有 pinning 或上下文的情况下轮询 Future 和 Stream。

**主要组成部分：**

*   **`spawn<T>(task: T) -> Spawn<T>`**:  这是一个创建 `Spawn` 实例的函数。它接收一个 Future 或 Stream 作为参数，并将其包装在一个模拟的执行器中。
*   **`Spawn<T>`**:  这个结构体是核心。它包装了一个 Future 或 Stream，并提供 `poll()` 和 `poll_next()` 方法，用于轮询内部的 Future 或 Stream。它还跟踪任务被唤醒的次数。
*   **`MockTask`**:  这是一个模拟的任务，用于提供上下文和唤醒机制。它包含一个 `ThreadWaker`，用于跟踪任务的唤醒状态。
*   **`ThreadWaker`**:  这个结构体负责管理任务的唤醒状态。它使用一个互斥锁和一个条件变量来同步唤醒操作。
*   **`IDLE`、`WAKE`、`SLEEP`**:  这些常量定义了 `ThreadWaker` 的状态。
*   **`VTABLE`**:  定义了 `RawWakerVTable`，用于创建 `Waker`。
*   **`to_raw`、`from_raw`、`clone`、`wake`、`wake_by_ref`、`drop_waker`**:  这些函数用于创建、克隆、唤醒和释放 `Waker`。

**工作原理：**

1.  `spawn()` 函数创建一个 `Spawn` 实例，并将传入的 Future 或 Stream 包装在其中。
2.  `Spawn` 结构体持有 `MockTask`，它提供了一个模拟的任务上下文。
3.  `poll()` 和 `poll_next()` 方法调用 `MockTask` 的 `enter()` 方法，该方法设置一个模拟的上下文，然后调用内部 Future 或 Stream 的 `poll()` 或 `poll_next()` 方法。
4.  `ThreadWaker` 跟踪任务的唤醒状态。当 Future 或 Stream 需要被唤醒时，它会调用 `wake()` 方法，该方法会设置 `ThreadWaker` 的状态为 `WAKE`。
5.  `is_woken()` 方法用于检查任务是否被唤醒。

**与其他部分的关联：**

*   这个文件是 `tokio-test` crate 的一部分，用于提供测试 Future 和 Stream 的工具。
*   `Spawn` 结构体可以与 `assert_ready_ok!`、`assert_ready_err!`、`assert_pending!` 和 `assert_ready_eq!` 等宏一起使用，用于断言 Future 或 Stream 的状态。
