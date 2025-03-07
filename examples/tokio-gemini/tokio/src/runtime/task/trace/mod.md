这个文件定义了用于 Tokio 运行时任务跟踪的结构和函数。它的主要目的是捕获和显示任务的执行轨迹，这对于调试和性能分析非常有用。

**关键组件：**

*   **`Context`**:  一个环境上下文，用于跟踪任务的调用栈。它使用 `Cell` 来存储当前活动的帧和收集器。
    *   `active_frame`:  一个 `Cell`，存储当前活动帧的地址。这用于建立回溯的上限。
    *   `collector`:  一个 `Cell`，存储 `Trace` 实例，用于收集回溯信息。
*   **`Frame`**:  表示调用栈中的一个帧。它构成了一个侵入式的双向链表。
    *   `inner_addr`:  与此帧关联的地址。
    *   `parent`:  父帧，如果存在。
*   **`Trace`**:  表示一个执行轨迹，包含一系列的回溯信息。
    *   `backtraces`:  一个 `Vec`，存储回溯信息。
*   **`Root<T>`**:  一个 Future 包装器，用于标记跟踪的根。
    *   `future`:  被包装的 Future。
*   **`trace_leaf`**:  如果这是 `Trace::capture` 的子调用，则捕获回溯信息。
*   **`trace_current_thread`**:  跟踪当前线程运行时中的所有任务。
*   **`trace_multi_thread`**:  跟踪多线程运行时中的所有任务（仅在启用 `rt-multi-thread` 功能时可用）。
*   **`trace_owned`**:  跟踪 `OwnedTasks`。

**功能：**

1.  **跟踪捕获 (`Trace::capture`)**:  捕获在给定闭包执行期间发生的回溯信息。它使用 `Context` 来管理回溯的上下文。
2.  **跟踪根 (`Trace::root`)**:  标记一个 Future 作为跟踪的根。
3.  **叶子跟踪 (`trace_leaf`)**:  捕获回溯信息，当它在 `Trace::capture` 内部被调用时。
4.  **任务跟踪**:  `trace_current_thread` 和 `trace_multi_thread` 函数用于跟踪运行时中的任务，并收集它们的执行轨迹。
5.  **回溯信息收集**:  `Trace` 结构体存储捕获的回溯信息。

**与其他部分的关联：**

*   与 `crate::runtime::context` 交互，用于访问线程本地存储中的跟踪上下文。
*   使用 `crate::task` 模块中的 `Id` 和 `Notified` 类型。
*   使用 `backtrace` crate 来捕获回溯信息。
*   与 `scheduler` 模块交互，用于在任务产生时调度唤醒。
*   `Root` 结构体用于包装 Future，并设置跟踪的根。

这个文件定义了 Tokio 运行时中用于任务跟踪的核心机制，允许捕获任务的执行轨迹，这对于调试和性能分析至关重要。
```
