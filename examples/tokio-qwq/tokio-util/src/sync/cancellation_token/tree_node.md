# `tree_node.rs` 文件详解

## 文件目的
该文件实现了 `CancellationToken` 的核心树结构逻辑，通过 `TreeNode` 结构体管理取消信号的传播和树节点的生命周期。它负责维护节点间的父子关系、处理取消请求的传播、以及动态调整树结构以保持最小化。

---

## 核心组件

### 1. **TreeNode 结构体**
```rust
pub(crate) struct TreeNode {
    inner: Mutex<Inner>,
    waker: tokio::sync::Notify,
}
```
- **`inner`**: 使用 `Mutex` 包裹的 `Inner` 结构体，包含节点的核心数据：
  - `parent`: 父节点的 `Arc<TreeNode>` 引用。
  - `children`: 所有子节点的 `Arc<TreeNode>` 列表。
  - `is_cancelled`: 标记节点是否已取消。
  - `num_handles`: 指向该节点的 `CancellationTokens` 数量。
- **`waker`**: 用于在取消时唤醒等待的异步任务。

### 2. **关键函数**
#### a. **节点创建与连接**
- **`child_node(parent: &Arc<TreeNode>) -> Arc<TreeNode>`**  
  创建父节点的子节点，并建立父子关系。若父节点已取消，则子节点直接标记为已取消。
- **`disconnect_children(node: &mut Inner)`**  
  断开节点与其所有子节点的连接，释放父子关系。

#### b. **取消操作**
- **`cancel(node: &Arc<TreeNode>)`**  
  递归取消节点及其所有后代：
  1. 断开子节点并直接连接到当前节点的父节点（避免遗漏）。
  2. 标记节点为已取消，并通知等待者。
- **`move_children_to_parent`**  
  将子节点转移到父节点，确保取消信号的传递。

#### c. **引用计数管理**
- **`increase_handle_refcount` / `decrease_handle_refcount`**  
  管理指向节点的 `CancellationTokens` 数量。当引用计数归零时：
  1. 将节点从树中移除。
  2. 将其子节点直接连接到父节点，保持树结构最小化。

#### d. **锁顺序与死锁安全**
- **`with_locked_node_and_parent`**  
  确保按节点创建顺序加锁（父节点先于子节点），通过循环重试机制避免死锁。依赖 **不变式 #2** 确保锁顺序正确。

---

## 核心逻辑与不变式
### 不变式（Invariant）
1. **无父节点且无引用的节点不可被取消**  
   确保无用节点及时从树中移除。
2. **子节点晚于父节点创建**  
   保证锁顺序（父节点先于子节点加锁），避免死锁。
3. **父节点解锁前恢复父子关系**  
   确保树结构在锁释放时保持正确。

### 死锁安全机制
- **锁顺序规则**：始终先锁父节点再锁子节点，通过 `with_locked_node_and_parent` 抽象实现。
- **循环重试机制**：在加锁失败时重试，确保最终能正确获取锁。

---

## 在项目中的角色