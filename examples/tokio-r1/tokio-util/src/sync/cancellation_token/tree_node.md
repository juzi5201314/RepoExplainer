# TreeNode Module Explanation

## Purpose
The `tree_node.rs` file implements the core tree structure for Tokio's `CancellationToken` system. It manages hierarchical cancellation propagation, where canceling a parent node triggers cancellation in all its descendants. The `TreeNode` struct encapsulates the tree logic, ensuring efficient and thread-safe operations.

## Key Components

### `TreeNode` Struct
- **Inner Data**: Wrapped in a `Mutex<Inner>` for thread-safe access.
  - `parent`: Optional reference to the parent node.
  - `children`: List of child nodes.
  - `is_cancelled`: Flag indicating cancellation status.
  - `num_handles`: Reference count for active `CancellationToken` handles.
- **Synchronization**: Uses `tokio::sync::Notify` to wake tasks waiting on cancellation.

### Core Functions
1. **Tree Construction**:
   - `child_node()`: Creates a child node linked to a parent. Skips linking if the parent is already canceled.
   - `move_children_to_parent()`: Reparents children when a node is removed to maintain tree connectivity.

2. **Refcounting**:
   - `increase_handle_refcount()`/`decrease_handle_refcount()`: Manage handle counts. When handles drop to zero, nodes detach from the tree.

3. **Cancellation Propagation**:
   - `cancel()`: Marks a node and all descendants as canceled. Adopts grandchildren to minimize tree depth changes and notifies waiters via `Notify`.

4. **Deadlock Prevention**:
   - `with_locked_node_and_parent()`: Ensures parent-child locking order (older nodes first) to avoid deadlocks. Handles edge cases where parent relationships change during locking.

### Invariants
1. **Orphaned Node Safety**: Nodes without parents/handles cannot be canceled.
2. **Creation Order**: Children are always younger than parents, dictating lock order.
3. **Structural Consistency**: Parent-child links are validated before releasing locks.

## Integration with Project
This module underpins the `CancellationToken` API in Tokio:
- `CancellationToken` acts as a lightweight handle to `TreeNode`.
- Hierarchical cancellation enables efficient propagation of cancel signals (e.g., stopping a task and all its subtasks).
- Used by async tasks to cooperatively check for cancellation via `is_cancelled()` and `notified()`.

## Role in the Project