这个文件定义了 Tokio 运行时中任务的核心组件。它包含了任务的结构体定义，以及与任务状态、调度、和内存管理相关的关键功能。

**主要组成部分：**

*   **`Cell<T: Future, S>`**: 这是任务的核心结构体，它包含了任务的所有组成部分。
    *   `header`: 包含任务的状态信息，例如状态、队列指针、虚函数表等。`Header` 必须是第一个字段，因为任务结构体会被 `*mut Cell` 和 `*mut Header` 引用。
    *   `core`: 包含任务的调度器、任务 ID 和任务的 `stage`。
    *   `trailer`: 包含冷数据，例如用于 `OwnedTasks` 的链表指针、`Waker` 和可选的钩子。
*   **`Core<T: Future, S>`**: 任务的核心部分，包含调度器、任务 ID 和任务的 `stage`。
*   **`Header`**: 任务的头部，包含任务的状态、队列指针、虚函数表、所有者 ID 和跟踪 ID。
*   **`Trailer`**: 任务的尾部，包含冷数据，例如链表指针、`Waker` 和钩子。
*   **`Stage<T: Future>`**: 任务的执行阶段，可以是 `Running` (运行中)、`Finished` (已完成) 或 `Consumed` (已消耗)。
*   **`CoreStage<T: Future>`**: 包含任务的 `stage`。
*   **`TaskIdGuard`**: 用于在执行 future 或 drop 时设置和清除上下文中的任务 ID。

**关键功能：**

*   **`Cell::new()`**: 创建一个新的任务单元，初始化 `Header`、`Core` 和 `Trailer`。
*   **`Core::poll()`**: 轮询 future。
*   **`Core::drop_future_or_output()`**: 释放 future。
*   **`Core::store_output()`**: 存储任务的输出。
*   **`Core::take_output()`**: 获取任务的输出。
*   **`Header` 的相关方法**:  用于获取 `Trailer`、调度器、ID 和跟踪 ID 的指针和值。
*   **`Trailer` 的相关方法**: 用于设置和获取 `Waker`，以及唤醒 join。

**与其他组件的交互：**

*   **`crate::future::Future`**:  任务执行的 future。
*   **`crate::runtime::task::Schedule`**: 任务的调度器。
*   **`crate::runtime::task::raw`**: 包含与任务相关的原始指针和虚函数表。
*   **`crate::runtime::task::state`**: 包含任务的状态信息。
*   **`crate::runtime::context`**: 用于设置和获取当前任务 ID。
*   **`crate::util::linked_list`**: 用于管理任务的链表。

**总结：**
