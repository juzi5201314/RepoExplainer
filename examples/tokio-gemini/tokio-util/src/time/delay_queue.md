该文件定义了一个名为 `DelayQueue` 的结构体，它是一个延迟元素队列。`DelayQueue` 允许将元素插入队列，并设置一个截止时间。当截止时间到达时，这些元素将通过 `poll_expired` 方法被返回。

**主要组成部分：**

*   **`DelayQueue<T>`**:  延迟队列的主结构体，其中 `T` 是存储的元素类型。
    *   `slab`:  使用 `slab::Slab` 存储与条目关联的数据，用于高效的内存分配和重用。
    *   `wheel`:  使用 `wheel::Wheel` 实现的定时器轮，用于跟踪队列中的延迟。
    *   `expired`:  一个栈，用于存储已经过期的延迟。
    *   `delay`:  一个 `tokio::time::Sleep` 的 `Pin<Box<>>`，用于跟踪队列中最早到期的延迟。
    *   `wheel_now`:  定时器轮的当前时间。
    *   `start`:  定时器开始的时刻。
    *   `waker`:  当需要重置定时器时调用的 `Waker`。
*   **`SlabStorage<T>`**:  用于管理 `slab` 的辅助结构体，处理键的重新映射，以应对 `compact` 操作。
    *   `inner`:  实际存储数据的 `slab::Slab`。
    *   `key_map`:  一个 `HashMap`，用于跟踪在 `compact` 调用期间重新映射的键。
    *   `next_key_index`:  用于创建新键的索引。
    *   `compact_called`:  一个布尔值，指示是否已调用 `compact`。
*   **`Expired<T>`**:  表示已过期并从队列中移除的条目。
    *   `data`:  存储在队列中的数据。
    *   `deadline`:  过期时间。
    *   `key`:  与条目关联的键。
*   **`Key`**:  用于标识 `DelayQueue` 中元素的令牌。
*   **`KeyInternal`**:  内部使用的键类型，用于在 `compact` 操作后进行键的重新映射。
*   **`Stack<T>`**:  用于管理过期元素的栈。
*   **`Data<T>`**:  存储在队列中的数据，包含实际数据、过期时间、过期状态以及用于栈的链接。

**功能：**

*   **`new()` 和 `with_capacity()`**:  创建新的 `DelayQueue` 实例。
*   **`insert_at()`**:  将元素插入队列，并指定过期时间点。
*   **`insert()`**:  将元素插入队列，并指定过期时间（相对于当前时间）。
*   **`poll_expired()`**:  轮询队列，返回已过期的元素。
*   **`deadline()`**:  获取给定键的截止时间。
*   **`remove()`**:  移除与给定键关联的元素。
*   **`try_remove()`**:  尝试移除与给定键关联的元素，如果不存在则返回 `None`。
*   **`reset_at()`**:  将给定键的过期时间重置为指定的时间点。
*   **`reset()`**:  将给定键的过期时间重置为相对于当前时间的持续时间。
*   **`shrink_to_fit()`**:  尝试减小 `slab` 的容量以适应当前元素数量。
*   **`compact()`**:  压缩 `slab`，回收已删除元素的空间。
*   **`peek()`**:  获取下一个将要过期的元素的键，但不移除它。
*   **`next_deadline()`**:  获取下一个到期时间。
*   **`clear()`**:  清空队列。
*   **`capacity()`**:  获取队列的容量。
*   **`len()`**:  获取队列中元素的数量。
*   **`reserve()`**:  预留额外的容量。
*   **`is_empty()`**:  检查队列是否为空。
*   **`poll_idx()`**:  轮询队列，返回下一个应该返回的 `slab` 中的槽的索引。
*   **`normalize_deadline()`**:  规范化截止时间。

**与其他组件的交互：**

*   使用 `wheel` 模块中的 `Wheel` 结构体来管理延迟。
*   使用 `slab` 模块中的 `Slab` 结构体来存储数据。
*   使用 `tokio::time` 模块中的 `sleep_until` 和 `Duration` 来处理时间。
*   实现 `futures_core::Stream` trait，使得 `DelayQueue` 可以作为异步流使用。

**整体项目中的作用：**
