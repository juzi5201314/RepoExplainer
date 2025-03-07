这个文件定义了一个名为 `TryJoin3` 的结构体和相关的函数，用于并发地执行三个 `Future`，并等待它们全部完成。它类似于 `join!` 宏，但专门处理返回 `Result` 的 `Future`，并在其中一个 `Future` 失败时立即返回错误。

**主要组成部分：**

1.  **`try_join3` 函数:**
    *   这是一个公共的（`pub(crate)`）函数，用于创建 `TryJoin3` 结构体的实例。
    *   它接受三个 `Future` 作为输入，每个 `Future` 都会产生一个 `Result` 类型的结果。
    *   它使用 `maybe_done` 函数将每个 `Future` 包装成 `MaybeDone` 类型。`MaybeDone` 用于跟踪 `Future` 是否已经完成，并缓存其结果。
    *   它返回一个 `TryJoin3` 结构体的实例，该实例封装了这三个 `MaybeDone` 类型的 `Future`。

2.  **`TryJoin3` 结构体:**
    *   使用 `pin_project!` 宏来创建，这允许安全地对结构体中的字段进行 `Pin` 操作。
    *   包含三个字段：`future1`、`future2` 和 `future3`，它们都是 `MaybeDone<F>` 类型，其中 `F` 是原始 `Future` 的类型。
    *   `#[pin]` 属性意味着这些字段可以被 `Pin` 住，这对于处理 `Future` 至关重要。

3.  **`Future` 的 `impl` 块 (针对 `TryJoin3`):**
    *   实现了 `Future` trait，使得 `TryJoin3` 本身也是一个 `Future`。
    *   `type Output = Result<(T1, T2, T3), E>;` 定义了 `TryJoin3` 的输出类型，如果所有三个 `Future` 都成功完成，则输出一个包含三个结果的元组 `(T1, T2, T3)`，如果其中任何一个 `Future` 失败，则输出一个错误 `E`。
    *   `poll` 方法是 `Future` trait 的核心。它负责轮询（poll）三个 `Future`，检查它们是否完成。
        *   它首先将 `self` 投影（project）到其字段上，以便安全地访问和操作被 `Pin` 住的 `Future`。
        *   它依次轮询 `future1`、`future2` 和 `future3`。
        *   如果任何一个 `Future` 返回错误，则立即返回该错误。
        *   如果所有 `Future` 都完成并且没有错误，则返回一个包含所有结果的元组。
        *   如果任何一个 `Future` 尚未完成，则返回 `Poll::Pending`，表示任务尚未完成。

**工作流程：**

1.  调用 `try_join3` 函数创建 `TryJoin3` 实例，并将三个 `Future` 传递给它。
2.  在某个 `tokio` 运行时中，`TryJoin3` 实例被轮询。
3.  `poll` 方法依次轮询三个 `Future`。
4.  如果任何一个 `Future` 产生错误，`poll` 方法立即返回该错误。
5.  如果所有 `Future` 都成功完成，`poll` 方法返回一个包含所有结果的元组。
6.  如果任何一个 `Future` 尚未完成，`poll` 方法返回 `Poll::Pending`，表示需要稍后再次轮询。

**与其他组件的关系：**

*   `maybe_done`:  `TryJoin3` 使用 `maybe_done` 函数包装每个 `Future`。`MaybeDone` 是一种包装器，用于跟踪 `Future` 是否已经完成，并缓存其结果。这允许 `TryJoin3` 在轮询时检查 `Future` 的状态，并避免重复执行已经完成的 `Future`。
*   `pin_project_lite`:  用于安全地对结构体中的字段进行 `Pin` 操作，这对于处理 `Future` 至关重要，因为 `Future` 可能会持有对自身或其他数据的引用。
*   `Future` trait:  `TryJoin3` 实现了 `Future` trait，使其可以被 `tokio` 运行时轮询和执行。
