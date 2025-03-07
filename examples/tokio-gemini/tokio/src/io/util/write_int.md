这个文件定义了一系列用于异步写入整数和浮点数的 Future。这些 Future 实现了 `AsyncWrite` trait，允许将各种整数和浮点数类型以二进制格式写入到实现了 `AsyncWrite` trait 的目标，例如网络连接或文件。

**关键组件：**

1.  **`writer!` 宏:**
    *   这个宏用于生成写入多字节整数和浮点数的 Future。
    *   它接受类型名称（例如 `WriteU32`），要写入的类型（例如 `u32`），`bytes` crate 中用于将值转换为字节序列的函数（例如 `put_u32`），以及可选的字节数。
    *   它使用 `pin_project!` 宏创建一个 `!Unpin` 的结构体，以确保与异步 trait 方法的兼容性。
    *   结构体包含一个目标写入器 (`dst`)，一个缓冲区 (`buf`) 用于存储要写入的字节，一个 `written` 字段用于跟踪已写入的字节数，以及一个 `PhantomPinned` 字段，以确保 Future 不可移动。
    *   `new` 方法创建一个新的 Future 实例，将给定的值转换为字节序列并存储在缓冲区中。
    *   `Future` 的 `poll` 方法尝试将缓冲区中的字节写入目标写入器。它循环写入，直到所有字节都已写入或发生错误。

2.  **`writer8!` 宏:**
    *   这个宏用于生成写入单字节整数的 Future。
    *   它接受类型名称（例如 `WriteU8`）和要写入的类型（例如 `u8`）。
    *   它类似于 `writer!` 宏，但简化了，因为它只需要写入一个字节。
    *   `new` 方法创建一个新的 Future 实例，将给定的值转换为一个字节。
    *   `Future` 的 `poll` 方法尝试将该字节写入目标写入器。

3.  **生成的 Future:**
    *   `WriteU8`, `WriteI8`: 用于写入 `u8` 和 `i8` 类型。
    *   `WriteU16`, `WriteU32`, `WriteU64`, `WriteU128`: 用于写入大端字节序的无符号整数。
    *   `WriteI16`, `WriteI32`, `WriteI64`, `WriteI128`: 用于写入大端字节序的有符号整数。
    *   `WriteF32`, `WriteF64`: 用于写入大端字节序的浮点数。
    *   `WriteU16Le`, `WriteU32Le`, `WriteU64Le`, `WriteU128Le`: 用于写入小端字节序的无符号整数。
    *   `WriteI16Le`, `WriteI32Le`, `WriteI64Le`, `WriteI128Le`: 用于写入小端字节序的有符号整数。
    *   `WriteF32Le`, `WriteF64Le`: 用于写入小端字节序的浮点数。

**如何融入项目：**

这个文件定义了一组用于将各种数值类型异步写入到实现了 `AsyncWrite` trait 的目标（如网络连接或文件）的 Future。这些 Future 可以被其他代码使用，例如在网络协议实现中，用于序列化数据并将其发送到网络。它们提供了方便且高效的方式来写入不同类型的数值，并处理异步写入操作。
