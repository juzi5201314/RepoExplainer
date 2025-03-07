这个文件定义了一个侵入式的双向链表，用于存储数据。它使用 `unsafe` 代码块来操作指针，因此需要调用者确保链表中的节点是有效的。

**关键组件：**

*   **`LinkedList<L, T>`**:  这是链表的主结构体。
    *   `head`:  链表的头节点。
    *   `tail`:  链表的尾节点。
    *   `_marker`:  一个 `PhantomData`，用于标记节点类型。
*   **`Link` trait**:  定义了如何在一个链表中跟踪一个类型。
    *   `Handle`:  链表条目的句柄。
    *   `Target`:  节点类型。
    *   `as_raw`:  将句柄转换为原始指针。
    *   `from_raw`:  将原始指针转换为句柄。
    *   `pointers`:  返回节点的指针。
*   **`Pointers<T>`**:  存储节点的“前驱”和“后继”指针。
    *   `inner`:  一个 `UnsafeCell`，包含 `PointersInner`。
*   **`PointersInner<T>`**:  实际存储前驱和后继指针的结构体。
    *   `prev`:  前一个节点。
    *   `next`:  后一个节点。
    *   `_pin`:  一个 `PhantomPinned` 字段，用于防止编译器对指针进行别名分析优化。
*   **`GuardedLinkedList<L, T>`**:  一个受保护的链表，它使用一个特殊的保护节点来确保链表是循环的。
*   **`DrainFilter<'a, T, F>`**:  一个迭代器，用于从链表中移除满足过滤条件的元素。

**功能：**

*   创建空链表 (`new`)。
*   在链表头部添加元素 (`push_front`)。
*   从链表头部移除元素 (`pop_front`)。
*   从链表尾部移除元素 (`pop_back`)。
*   检查链表是否为空 (`is_empty`)。
*   从链表中移除指定的节点 (`remove`)。
*   将链表转换为受保护的链表 (`into_guarded`)。
*   使用过滤器移除元素 (`drain_filter`)。
*   遍历链表中的每个元素 (`for_each`)。

**与其他部分的关联：**

*   `Link` trait 允许将不同类型的节点存储在链表中。
*   `Pointers` 结构体用于存储链表节点的前驱和后继指针。
*   `GuardedLinkedList` 提供了链表的另一种实现，它使用一个保护节点来确保链表是循环的。
*   `DrainFilter` 允许从链表中移除满足特定条件的元素。
*   `tests` 模块包含单元测试，用于验证链表的功能。
