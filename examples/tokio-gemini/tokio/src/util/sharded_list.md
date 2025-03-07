这个文件定义了一个名为 `ShardedList` 的结构体，它是一个支持高并发更新的侵入式链表。它通过分片设计来提高并发性能，将链表分成多个部分（分片），每个分片由一个互斥锁保护。

**关键组件：**

*   `ShardedList<L, T>`：
    *   `lists`: 一个 `Mutex` 组成的 `Box<[]>`，每个 `Mutex` 保护一个 `LinkedList`，构成链表的分片。
    *   `added`:  `MetricAtomicU64`，用于原子地记录添加到链表的元素总数。
    *   `count`:  `MetricAtomicUsize`，用于原子地记录链表中元素的总数。
    *   `shard_mask`:  `usize`，用于计算分片 ID 的掩码。
*   `ShardedListItem`:  一个 `unsafe trait`，定义了如何确定一个元素应该存储在哪个分片中。`get_shard_id` 方法必须保证对于一个给定的元素，其分片 ID 在整个生命周期内保持不变。
*   `ShardGuard<'a, L, T>`：一个结构体，用于获取分片的锁，并提供对分片链表的访问权限。它持有 `MutexGuard`，以及对 `added` 和 `count` 的引用。
*   `new(sharded_size: usize)`：构造函数，创建一个新的 `ShardedList`。`sharded_size` 必须是 2 的幂。
*   `pop_back(&self, shard_id: usize) -> Option<L::Handle>`：从指定分片中移除最后一个元素。
*   `remove(&self, node: NonNull<L::Target>) -> Option<L::Handle>`：从链表中移除指定的节点。
*   `lock_shard(&self, val: &L::Handle) -> ShardGuard<'_, L, L::Target>`：获取指定元素的所在分片的锁，并返回一个 `ShardGuard`。
*   `len(&self) -> usize`：获取链表中元素的总数。
*   `added(&self) -> u64`：获取添加到链表的元素总数（仅在启用 `cfg_64bit_metrics` 特性时可用）。
*   `is_empty(&self) -> bool`：检查链表是否为空。
*   `shard_size(&self) -> usize`：获取分片的大小。
*   `shard_inner(&self, id: usize) -> MutexGuard<'_, LinkedList<L, <L as Link>::Target>>`：获取指定分片的 `MutexGuard`。
*   `push(mut self, val: L::Handle)`：将一个元素推入到 `ShardGuard` 锁定的分片中。
*   `for_each<F>(&self, mut f: F)`：对链表中的每个元素执行给定的函数（仅在启用 `cfg_taskdump` 特性时可用）。

**工作原理：**

1.  **分片：** `ShardedList` 将链表分成多个分片，每个分片由一个 `Mutex` 保护。
2.  **分片 ID：**  `ShardedListItem` trait 的 `get_shard_id` 方法用于确定一个元素应该存储在哪个分片中。
3.  **并发控制：**  当需要访问或修改链表时，首先使用 `lock_shard` 获取对应分片的锁。由于每个分片都有自己的锁，因此不同分片的并发操作可以并行执行，从而提高并发性能。
4.  **原子计数：**  `added` 和 `count` 使用原子操作来维护链表中元素的总数，确保在并发环境下的正确性。

**与其他组件的关联：**

*   `LinkedList`：`ShardedList` 使用 `LinkedList` 作为其内部数据结构，每个分片都包含一个 `LinkedList`。
*   `Mutex`：用于保护每个分片，确保线程安全。
*   `MetricAtomicU64` 和 `MetricAtomicUsize`：用于原子地记录链表的状态信息。
*   `loom`：用于并发测试。
