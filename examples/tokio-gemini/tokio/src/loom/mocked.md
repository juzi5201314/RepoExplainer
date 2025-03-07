这个文件 `mocked.rs` 位于 `tokio` 项目的 `loom` 模块中，其主要目的是为 Tokio 项目提供一个模拟（mocked）的并发原语和系统调用，以便在测试和模拟环境中进行并发相关的代码测试。它通过使用 `loom` crate 来模拟并发行为，`loom` 是一个用于并发测试的 Rust 库，它提供了一种确定性的并发模拟环境。

以下是该文件的关键组成部分：

1.  **`pub(crate) use loom::*;`**:  将 `loom` crate 中的所有内容引入当前模块，使得可以直接使用 `loom` 提供的各种功能。

2.  **`pub(crate) mod sync`**:  定义了一个 `sync` 模块，该模块模拟了常见的并发同步原语，如互斥锁（Mutex）和读写锁（RwLock）。
    *   **`Mutex<T>`**:  模拟了互斥锁，基于 `loom::sync::Mutex` 实现。提供了 `new`, `lock`, `try_lock`, 和 `get_mut` 方法，分别用于创建、加锁、尝试加锁和获取可变引用。
    *   **`RwLock<T>`**:  模拟了读写锁，基于 `loom::sync::RwLock` 实现。提供了 `new`, `read`, `try_read`, `write`, 和 `try_write` 方法，分别用于创建、读取、尝试读取、写入和尝试写入。
    *   **`pub(crate) use loom::sync::*;`**: 再次引入 `loom::sync` 模块中的所有内容，可能用于简化代码。
    *   **`pub(crate) mod atomic`**:  定义了一个 `atomic` 模块，模拟了原子操作。
        *   **`StaticAtomicU64`**:  使用 `std::sync::atomic::AtomicU64` 作为 `StaticAtomicU64` 的实现，这表明在模拟环境中，它使用标准库的原子类型。

3.  **`pub(crate) mod rand`**:  定义了一个 `rand` 模块，模拟了随机数生成。
    *   **`seed()`**:  提供了一个固定的种子值 `1`，这确保了在模拟环境中随机数生成是可预测的，从而方便测试。

4.  **`pub(crate) mod sys`**:  定义了一个 `sys` 模块，模拟了系统相关的信息。
    *   **`num_cpus()`**:  返回一个固定的 CPU 数量 `2`，这允许模拟多核环境。

5.  **`pub(crate) mod thread`**:  定义了一个 `thread` 模块，模拟了线程相关的功能。
    *   **`pub use loom::lazy_static::AccessError;`**: 引入了 `loom::lazy_static::AccessError`，用于处理静态变量的访问错误。
    *   **`pub use loom::thread::*;`**: 引入了 `loom::thread` 模块中的所有内容，可能包括线程创建、同步等功能。
