这个文件定义了一个名为 `Either` 的泛型枚举类型，用于将两个具有相同关联类型的不同异步类型（如 Future、Stream 或 Sink）组合成一个单一类型。这在需要根据条件选择使用哪个异步操作时非常有用，例如在 `if/else` 语句中。

**关键组件：**

*   **`Either<L, R>` 枚举:**  定义了 `Left` 和 `Right` 两个变体，分别持有类型 `L` 和 `R` 的值。`L` 和 `R` 通常是不同的异步类型，但它们必须具有相同的输出类型（对于 `Future`）或相同的 `Item` 类型（对于 `Stream`）和 `Error` 类型（对于 `Sink`）。
*   **`delegate_call!` 宏:**  这是一个辅助宏，用于简化异步 trait 方法的实现。它接收一个方法调用作为参数，并根据 `Either` 枚举的当前变体（`Left` 或 `Right`）将调用转发到相应的内部类型。这避免了在每个 trait 实现中重复的 `match` 语句。
*   **异步 trait 实现:**  为 `Either` 实现了多个异步 trait，包括 `Future`、`AsyncRead`、`AsyncBufRead`、`AsyncSeek`、`AsyncWrite`、`Stream` 和 `Sink`。这些实现通过 `delegate_call!` 宏将方法调用委托给内部的 `L` 或 `R` 类型。

**与其他组件的交互：**

*   **与 `tokio` 的集成:**  `Either` 实现了 `tokio::io` 模块中的异步 trait，使其可以与 Tokio 的 I/O 操作无缝集成。
*   **与 `futures` 的集成:**  `Either` 也实现了 `futures_core::stream::Stream` 和 `futures_sink::Sink` trait，使其可以与 `futures` crate 中的流和 sink 操作一起使用。
*   **在项目中的作用:**  `Either` 允许在需要根据运行时条件选择不同异步操作的场景中，将这些操作统一为一个类型。这简化了代码，并提高了灵活性。例如，在处理网络请求时，可以根据请求类型选择使用不同的异步读取器，然后使用 `Either` 将它们统一为一个类型。
