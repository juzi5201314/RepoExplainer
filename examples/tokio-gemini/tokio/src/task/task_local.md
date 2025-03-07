这个文件定义了 Tokio 任务本地存储相关的结构体、宏和实现。它的主要目的是提供一种机制，允许在 Tokio 任务中存储和访问特定于任务的数据，类似于线程本地存储，但作用域限定在单个任务内。

**关键组件：**

1.  **`task_local!` 宏：**
    *   这是一个宏，用于声明新的任务本地键，类型为 [`tokio::task::LocalKey`]。
    *   它接受静态声明作为输入，并使这些静态变量对当前任务是本地的。
    *   宏内部使用 `__task_local_inner!` 宏来创建 `LocalKey` 实例，并将其存储在线程本地存储中。

2.  **`__task_local_inner!` 宏：**
    *   这是一个内部宏，由 `task_local!` 宏调用。
    *   它创建 `LocalKey` 类型的静态变量。
    *   它使用 `std::thread_local!` 宏创建一个线程本地存储，用于存储任务本地值。
    *   每个 `LocalKey` 实例都包含一个 `thread::LocalKey<RefCell<Option<T>>>`，其中 `RefCell` 用于在运行时进行可变借用检查，`Option<T>` 用于存储实际的值。

3.  **`LocalKey<T>` 结构体：**
    *   表示一个任务本地键。
    *   它包含一个 `thread::LocalKey`，用于访问线程本地存储中的值。
    *   `scope()` 方法：设置一个值作为 future `F` 的任务本地值。当 `scope` 完成时，任务本地值将被丢弃。
    *   `sync_scope()` 方法：设置一个值作为闭包 `F` 的任务本地值。当 `sync_scope` 完成时，任务本地值将被丢弃。
    *   `with()` 方法：访问当前任务本地值，并运行提供的闭包。如果任务本地值未设置，则会 panic。
    *   `try_with()` 方法：访问当前任务本地值，并运行提供的闭包。如果任务本地值未设置，则返回 `AccessError`。
    *   `get()` 方法：如果任务本地值实现了 `Clone`，则返回任务本地值的副本。如果任务本地值未设置，则会 panic。

4.  **`TaskLocalFuture<T, F>` 结构体：**
    *   一个 future，在执行期间设置任务本地值。
    *   由 `LocalKey::scope` 方法创建。
    *   它持有任务本地键、值和 future。
    *   当 future 被轮询时，它会设置任务本地值，并运行内部的 future。
    *   `take_value()` 方法：获取任务本地值，并将其从 `TaskLocalFuture` 中移除。

5.  **`AccessError` 结构体：**
    *   一个错误类型，由 `LocalKey::try_with` 方法返回，表示无法访问任务本地值。

6.  **`ScopeInnerErr` 枚举：**
    *   一个内部错误类型，用于 `scope_inner` 方法。

**工作原理：**

1.  使用 `task_local!` 宏声明一个任务本地键。
2.  使用 `LocalKey::scope` 或 `LocalKey::sync_scope` 设置任务本地值。
3.  在 `scope` 或 `sync_scope` 的闭包或 future 中，使用 `LocalKey::with` 或 `LocalKey::try_with` 访问任务本地值。
4.  当 `scope` 或 `sync_scope` 完成时，任务本地值将被自动丢弃。

**与其他组件的交互：**

*   与 Tokio 运行时紧密集成，用于在任务的执行过程中管理任务本地存储。
*   使用 `pin_project_lite` crate 来实现 `TaskLocalFuture` 的自引用结构。
*   使用 `std::thread_local!` 来存储任务本地值，但作用域限定在单个任务内。
