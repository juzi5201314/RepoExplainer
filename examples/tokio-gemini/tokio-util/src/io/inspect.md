这个文件定义了两个结构体 `InspectReader` 和 `InspectWriter`，它们是用于在异步读写操作中检查数据的适配器。它们都使用了 `pin_project_lite` 宏来确保结构体成员在 `Pin` 之后是不可移动的。

**`InspectReader` 结构体:**

*   **目的:** 允许在读取数据时检查数据。这对于例如在读取数据时进行哈希计算非常有用。
*   **组成部分:**
    *   `reader`: 一个被包装的 `AsyncRead` 类型的对象，用于实际的读取操作。
    *   `f`: 一个闭包或函数，它接受一个 `&[u8]` 类型的切片作为参数，该切片包含每次读取操作中新读取的数据。
*   **`new` 方法:** 创建一个新的 `InspectReader`，包装给定的 `reader`，并为每次读取调用提供一个闭包 `f`。
*   **`into_inner` 方法:** 消耗 `InspectReader`，返回被包装的 `reader`。
*   **`AsyncRead` 的实现:**
    *   `poll_read` 方法：重写了 `AsyncRead` trait 的 `poll_read` 方法。在调用底层 `reader` 的 `poll_read` 方法读取数据后，它会调用闭包 `f`，并将新读取的数据（从上次读取结束的位置到当前读取结束的位置）传递给它。

**`InspectWriter` 结构体:**

*   **目的:** 允许在写入数据时检查数据。这对于例如在写入数据时进行哈希计算非常有用。
*   **组成部分:**
    *   `writer`: 一个被包装的 `AsyncWrite` 类型的对象，用于实际的写入操作。
    *   `f`: 一个闭包或函数，它接受一个 `&[u8]` 类型的切片作为参数，该切片包含每次写入操作中成功写入的数据。
*   **`new` 方法:** 创建一个新的 `InspectWriter`，包装给定的 `writer`，并为每次写入调用提供一个闭包 `f`。
*   **`into_inner` 方法:** 消耗 `InspectWriter`，返回被包装的 `writer`。
*   **`AsyncWrite` 的实现:**
    *   `poll_write` 方法：重写了 `AsyncWrite` trait 的 `poll_write` 方法。在调用底层 `writer` 的 `poll_write` 方法写入数据后，如果写入成功，它会调用闭包 `f`，并将成功写入的数据传递给它。
    *   `poll_flush`, `poll_shutdown`, `poll_write_vectored`, `is_write_vectored` 方法：这些方法直接委托给底层的 `writer`。
*   **`AsyncRead` 的实现:**
    *   `poll_read` 方法：直接委托给底层的 `writer`。

**总结:**

这两个结构体通过包装现有的 `AsyncRead` 和 `AsyncWrite` 对象，并在读写操作前后调用用户提供的闭包，从而允许用户在不修改底层读写逻辑的情况下，对数据进行检查或处理。
