这个文件定义了一个名为 `Stack` 的 trait，它抽象了用于跟踪超时操作所需的栈操作。这个 trait 旨在提供一个通用的接口，用于管理存储在时间轮中的超时项。

**关键组件：**

*   `trait Stack: Default`: 定义了 `Stack` trait，并要求实现该 trait 的类型必须实现 `Default` trait。
*   `type Owned: Borrow<Self::Borrowed>`: 定义了栈中拥有的项的类型，它必须能够借用为 `Borrowed` 类型。
*   `type Borrowed: Eq + Hash`: 定义了借用的项的类型，它必须实现 `Eq` 和 `Hash` trait，以便进行比较和哈希操作。
*   `type Store`: 定义了用于存储栈中项的存储类型，例如可以使用 slab 分配器。
*   `fn is_empty(&self) -> bool`: 检查栈是否为空。
*   `fn push(&mut self, item: Self::Owned, store: &mut Self::Store)`: 将一个项推入栈中。
*   `fn pop(&mut self, store: &mut Self::Store) -> Option<Self::Owned>`: 从栈中弹出一个项。
*   `fn peek(&self) -> Option<Self::Owned>`: 窥视栈顶的项，但不移除它。
*   `fn remove(&mut self, item: &Self::Borrowed, store: &mut Self::Store)`: 从栈中移除一个特定的项。
*   `fn when(item: &Self::Borrowed, store: &Self::Store) -> u64`: 获取一个项的超时时间。

**与其他部分的关联：**

这个 `Stack` trait 被设计为时间轮（`wheel`）组件的一部分，用于管理超时事件。时间轮使用栈来存储和组织这些事件，以便高效地处理超时。`Stack` trait 提供了抽象，允许使用不同的栈实现（例如，基于堆的栈或基于 slab 的栈），而无需修改时间轮的核心逻辑。`Store` 类型允许使用更高效的存储方式，例如 `SlabStorage`。
