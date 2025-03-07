这个文件定义了用于支持工作窃取调度器的运行队列结构。它包含 `Local` 和 `Steal` 两种句柄，分别用于生产者（单个线程）和消费者（多个线程）。

**关键组件：**

*   **`UnsignedShort`，`UnsignedLong`，`AtomicUnsignedShort`，`AtomicUnsignedLong`**:  根据编译时是否支持 `atomic_u64`，定义了用于存储队列索引的无符号短整型和长整型，以及对应的原子类型。使用更宽的整数类型是为了提高 ABA 问题的弹性。
*   **`Local<T>`**: 生产者句柄，只能由单个线程使用。
*   **`Steal<T>`**: 消费者句柄，可以被多个线程使用，用于窃取任务。
*   **`Inner<T>`**: 核心结构，包含队列的实际数据。
    *   `head`:  原子长整型，由多个线程并发更新。包含两个 `UnsignedShort` 值。低位字节是队列的“真实”头部。高位字节由窃取者设置，表示正在窃取的第一个值。跟踪正在进行的窃取操作可以防止环绕场景。
    *   `tail`:  原子短整型，仅由生产者线程更新，但被多个线程读取。
    *   `buffer`:  `Box<[UnsafeCell<MaybeUninit<task::Notified<T>>>]>`，存储任务的缓冲区。使用 `UnsafeCell` 允许在没有 `&mut` 引用的情况下修改任务。
    *   `mask`:  `usize`，用于计算缓冲区索引的掩码。
*   **`local<T>(capacity: usize)`**:  创建一个新的本地运行队列，返回 `Steal<T>` 和 `Local<T>` 句柄。
*   **`remaining_slots()`**:  返回队列中可以推送任务的剩余槽位数量。
*   **`max_capacity()`**:  返回队列的最大容量。
*   **`is_empty()`**:  如果队列中没有条目，则返回 `true`。
*   **`can_steal()`**:  如果剩余槽位数量大于等于最大容量的一半，则返回 `true`。
*   **`push_back(tasks: impl ExactSizeIterator<Item = task::Notified<T>>)`**:  将一批任务推送到队列的末尾。如果队列没有足够的容量，则会 panic。
*   **`push_back_or_overflow<O: Overflow<T>>(task: task::Notified<T>, overflow: &O, stats: &mut Stats)`**:  将任务推送到队列的末尾。如果队列没有足够的容量，则将当前队列内容的一半移动到给定的注入队列。
*   **`pop()`**:  从本地队列中弹出一个任务。
*   **`steal_into(dst: &mut Local<T>, dst_stats: &mut Stats)`**:  从当前队列窃取一半的任务，并将它们放入目标队列。
*   **`steal_into2(&self, dst: &mut Local<T>, dst_tail: UnsignedShort)`**:  将任务从当前队列窃取到目标队列。
*   **`unpack(n: UnsignedLong)`**:  将 `head` 值拆分为真实头部和窃取者正在处理的索引。
*   **`pack(steal: UnsignedShort, real: UnsignedShort)`**:  将两个头部值合并。

**工作原理：**

该文件实现了用于多线程环境下的工作窃取调度器的核心数据结构。`Local` 队列由单个线程拥有，用于添加任务。`Steal` 队列可以被其他线程窃取任务。当一个线程的 `Local` 队列为空时，它会尝试从其他线程的 `Steal` 队列中窃取任务。为了避免竞争条件，使用了原子操作来管理队列的头部和尾部。当队列满时，`push_back_or_overflow` 函数会将队列中的一部分任务移动到注入队列，从而为新任务腾出空间。

**与其他文件的关系：**

这个文件是 Tokio 运行时调度器的一部分，它与 `task` 模块（定义了任务类型）和 `Overflow` trait（定义了溢出处理逻辑）等其他模块交互。它为多线程调度器提供了任务队列，并支持任务的添加、弹出和窃取操作。
