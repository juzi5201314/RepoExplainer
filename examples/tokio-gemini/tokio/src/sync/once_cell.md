这个文件定义了 `OnceCell`，一个线程安全的单元，它只能被写入一次。它在 Tokio 中用于需要首次使用时初始化一次但不需要进一步更改的全局变量。

**主要组成部分：**

*   `value_set`:  一个 `AtomicBool`，指示 `OnceCell` 是否已初始化。
*   `value`:  一个 `UnsafeCell<MaybeUninit<T>>`，用于存储实际的值。使用 `MaybeUninit` 允许在初始化之前存储未初始化的数据。`UnsafeCell` 允许在没有共享引用的情况下进行内部可变性。
*   `semaphore`:  一个 `Semaphore`，用于控制对 `value` 的访问和初始化。它确保只有一个线程可以初始化 `OnceCell`。

**关键方法：**

*   `new()`:  创建一个新的空的 `OnceCell`。
*   `const_new()`:  创建一个新的空的 `OnceCell`，可以在静态变量中使用。
*   `new_with(value: Option<T>)`:  创建一个新的 `OnceCell`，如果提供了值，则包含该值。
*   `const_new_with(value: T)`:  创建一个新的 `OnceCell`，包含提供的值，可以在静态变量中使用。
*   `initialized()`:  如果 `OnceCell` 包含一个值，则返回 `true`，否则返回 `false`。
*   `get()`:  返回对 `OnceCell` 中值的引用，如果已初始化，则返回 `Some(&T)`，否则返回 `None`。
*   `get_mut()`:  返回对 `OnceCell` 中值的可变引用，如果已初始化，则返回 `Some(&mut T)`，否则返回 `None`。
*   `set(value: T)`:  如果 `OnceCell` 为空，则将值设置为给定值。如果已经初始化，则返回错误。
*   `get_or_init<F, Fut>(f: F)`:  获取 `OnceCell` 中的值，如果尚未初始化，则使用给定的异步操作进行初始化。
*   `get_or_try_init<E, F, Fut>(f: F)`:  获取 `OnceCell` 中的值，如果尚未初始化，则使用给定的异步操作进行初始化，该操作可能返回一个 `Result`。
*   `into_inner()`:  从单元中取出值，销毁单元。如果单元为空，则返回 `None`。
*   `take()`:  获取当前值的所有权，使单元为空。如果单元为空，则返回 `None`。

**工作原理：**

`OnceCell` 使用信号量和原子布尔值来确保线程安全。当一个线程想要访问或初始化 `OnceCell` 时，它首先检查 `value_set`。如果为 `true`，则该值已初始化，线程可以直接访问它。如果为 `false`，则线程尝试获取信号量的许可。如果成功，则该线程可以安全地初始化 `value`。在初始化完成后，`value_set` 设置为 `true`，信号量关闭，以防止其他线程再次初始化该值。

**与其他组件的关联：**

*   `Semaphore`:  用于同步对 `OnceCell` 的访问。
*   `loom::cell::UnsafeCell`:  用于存储值，允许在没有共享引用的情况下进行内部可变性。
*   `std::sync::atomic`:  用于原子操作，确保线程安全。
*   `std::future`:  用于异步初始化。
