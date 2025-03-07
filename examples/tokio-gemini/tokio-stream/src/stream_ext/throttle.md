这个文件实现了 `tokio-stream` 库中的 `throttle` 功能，用于限制流中元素的产生速率，即在每个元素之间强制添加一个延迟。

**主要组成部分：**

1.  **`throttle` 函数:**
    *   这是一个公共函数，用于创建 `Throttle` 结构体的实例。
    *   它接受一个 `Duration` 参数，表示元素之间的延迟时间，以及一个实现了 `Stream` trait 的流作为输入。
    *   它初始化 `Throttle` 结构体的各个字段，包括一个用于延迟的 `Sleep` 对象，延迟时间 `duration`，一个标志 `has_delayed` 用于指示延迟是否已经完成，以及要进行限速的流 `stream`。

2.  **`Throttle` 结构体:**
    *   这是一个结构体，实现了 `Stream` trait，用于包装原始流并添加限速功能。
    *   `delay`:  一个 `Sleep` 对象，用于实现延迟。
    *   `duration`:  `Duration` 类型，表示延迟的时间长度。
    *   `has_delayed`:  一个布尔值，指示延迟是否已经完成。当 `delay` 已经准备好，但 `stream` 还没有被 poll 时，该值为 `true`。
    *   `stream`:  要进行限速的原始流。

3.  **`Throttle` 结构体的方法:**
    *   `get_ref()`:  获取对底层流的引用。
    *   `get_mut()`:  获取对底层流的可变引用。
    *   `into_inner()`:  消耗 `Throttle` 结构体，返回底层的流。

4.  **`Stream` trait 的实现 ( `impl<T: Stream> Stream for Throttle<T>` ):**
    *   `poll_next()`:  这是 `Throttle` 结构体实现 `Stream` trait 的核心方法。
        *   首先，它检查是否需要进行延迟。如果 `has_delayed` 为 `false` 并且延迟时间不为零，则等待 `delay` 完成。
        *   然后，它调用底层流的 `poll_next()` 方法来获取下一个元素。
        *   如果获取到了一个元素，并且延迟时间不为零，则重置 `delay` 以开始新的延迟。
        *   最后，将 `has_delayed` 设置为 `false`，并返回从底层流获取到的元素。
    *   `is_zero()`:  一个辅助函数，用于检查 `Duration` 是否为零。

**工作原理：**

`throttle` 函数通过在每次从底层流获取元素后引入一个延迟来实现限速。`poll_next` 方法首先检查是否需要等待延迟。如果需要，它会等待 `tokio::time::sleep_until` 完成。然后，它从底层流中获取下一个元素。在获取到元素后，它会重置 `delay` 以开始新的延迟。这样，每个元素之间就会强制间隔 `duration` 指定的时间。

**与项目的关系：**
