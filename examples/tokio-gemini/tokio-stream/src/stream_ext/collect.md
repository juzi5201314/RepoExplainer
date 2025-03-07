这个文件定义了 `Collect` 结构体和相关的 trait，用于将一个 `Stream` 收集到一个具体的集合类型中。

**主要组成部分：**

1.  **`Collect` 结构体:**
    *   这是一个 `Future`，由 `StreamExt::collect` 方法返回。
    *   它持有被收集的 `Stream`，以及一个用于存储收集结果的 `collection`。
    *   `_pin: PhantomPinned` 用于确保 `Collect` 不可 `Unpin`，以兼容异步 trait 方法。
    *   `pin_project!` 宏用于创建 `Collect` 结构的投影，方便在 `poll` 方法中安全地访问和修改其字段。

2.  **`FromStream` trait:**
    *   这个 trait 定义了如何从一个 `Stream` 转换成一个具体的集合类型。
    *   它包含一个 `sealed` 模块，用于防止第三方实现该 trait，以保证未来的扩展性。
    *   `FromStream` trait 本身没有定义任何方法，它的功能由 `sealed::FromStreamPriv` trait 实现。

3.  **`sealed::FromStreamPriv` trait:**
    *   这个 trait 包含实际的转换逻辑。
    *   `InternalCollection`: 中间类型，用于在收集过程中存储数据。
    *   `initialize`: 初始化集合，根据 `Stream` 的 `size_hint` 来预分配容量。
    *   `extend`: 将 `Stream` 的一个元素添加到集合中。
    *   `finalize`: 将中间集合转换为最终的集合类型。

4.  **`Collect` 的 `new` 方法:**
    *   创建一个新的 `Collect` 实例。
    *   初始化 `collection`，使用 `Stream` 的 `size_hint` 来预估容量。

5.  **`Collect` 的 `Future` 实现:**
    *   `poll` 方法是 `Collect` 的核心逻辑。
    *   它循环调用 `stream.poll_next` 来获取 `Stream` 中的元素。
    *   对于每个元素，它调用 `U::extend` 将元素添加到 `collection` 中。
    *   如果 `stream` 结束，或者 `extend` 返回 `false`（表示收集失败），则调用 `U::finalize` 将 `collection` 转换为最终结果，并返回 `Ready`。

6.  **`FromStream` 的实现:**
    *   为 `()`、`String`、`Vec<T>`、`Box<[T]>` 和 `Result<U, E>` 实现了 `FromStream` trait。
    *   这些实现定义了如何将 `Stream` 的元素收集到对应的集合类型中。

**文件在项目中的作用：**
