这个文件定义了 `CancellationToken` 内部树结构的核心逻辑，即 `TreeNode`。`CancellationToken` 本身只是轻量级的句柄，持有对 `TreeNode` 的引用，而所有取消操作的实际逻辑都由 `TreeNode` 实现。

**关键组件：**

*   **`TreeNode` 结构体：** 表示取消树中的一个节点。它包含一个互斥锁 (`Mutex`)，用于保护内部数据 `Inner`，以及一个 `tokio::sync::Notify`，用于在节点被取消时唤醒等待者。
*   **`Inner` 结构体：** 包含 `TreeNode` 的实际数据，包括：
    *   `parent`: 可选的父节点 (`Arc<TreeNode>`)。
    *   `parent_idx`: 父节点中子节点的索引。
    *   `children`: 子节点列表 (`Vec<Arc<TreeNode>>`)。
    *   `is_cancelled`: 一个布尔值，指示节点是否已被取消。
    *   `num_handles`: 节点的句柄数量。
*   **`is_cancelled(node: &Arc<TreeNode>) -> bool`：** 检查节点是否已被取消。
*   **`child_node(parent: &Arc<TreeNode>) -> Arc<TreeNode>`：** 创建一个子节点，并将其添加到父节点的子节点列表中。如果父节点已取消，则新创建的子节点也会被标记为已取消。
*   **`disconnect_children(node: &mut Inner)`：** 断开节点与其所有子节点的连接。
*   **`with_locked_node_and_parent<F, Ret>(node: &Arc<TreeNode>, func: F) -> Ret`：**  安全地获取节点及其父节点的锁，以避免死锁。该函数确保按照创建顺序锁定节点，并处理父节点可能在锁定过程中发生变化的情况。
*   **`move_children_to_parent(node: &mut Inner, parent: &mut Inner)`：** 将节点的所有子节点移动到其父节点。
*   **`remove_child(parent: &mut Inner, mut node: MutexGuard<'_, Inner>)`：** 从父节点中移除一个子节点。
*   **`increase_handle_refcount(node: &Arc<TreeNode>)`：** 增加节点的句柄引用计数。
*   **`decrease_handle_refcount(node: &Arc<TreeNode>)`：** 减少节点的句柄引用计数。当句柄计数降为 0 时，节点将从树中移除，其子节点将移动到其父节点。
*   **`cancel(node: &Arc<TreeNode>)`：** 取消一个节点及其所有子节点。该函数会递归地取消子节点，并处理子节点拥有子节点的情况。

**与项目的关系：**

这个文件实现了 `CancellationToken` 的核心数据结构和取消逻辑。它定义了取消树的结构，处理节点之间的父子关系，并确保在取消操作和引用计数管理过程中保持数据一致性和避免死锁。`CancellationToken` 结构体使用 `TreeNode` 来管理取消状态和传播取消信号。
