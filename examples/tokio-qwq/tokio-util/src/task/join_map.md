# `join_map.rs` 文件详解

## 文件目的
`JoinMap` 是 Tokio 生态中的一个任务管理工具，用于在 Tokio 运行时中管理一组异步任务，并为每个任务关联一个键（Key）。它扩展了 Tokio 的 `JoinSet` 功能，允许通过键取消任务、检查任务是否存在，并在任务完成时返回其关联的键和结果。该结构体特别适用于需要按键管理任务的场景。

---

## 核心组件
### 1. **结构体定义**
```rust
pub struct JoinMap<K, V, S = RandomState> {
    tasks_by_key: HashMap<Key<K>, AbortHandle, S>,
    hashes_by_task: HashMap<Id, u64, S>,
    tasks: JoinSet<V>,
}
```
- **`tasks_by_key`**：使用 `Key<K>`（包含用户提供的键和任务 ID）作为键，存储 `AbortHandle`，用于通过键查找任务。
- **`hashes_by_task`**：通过任务 ID 映射到键的哈希值，用于在任务完成时反向查找其键。
- **`tasks`**：底层使用 Tokio 的 `JoinSet` 管理任务的执行和完成。

### 2. **辅助结构 `Key<K>`**
```rust
struct Key<K> {
    key: K,
    id: Id,
}
```
- **作用**：解决哈希冲突。当多个任务的键哈希相同时，通过任务 ID 区分不同任务。

---

## 关键方法
### 1. **任务管理**
- **`spawn`/`spawn_on`/`spawn_blocking`**：  
  向 `JoinMap` 中添加任务，并关联键。若已有相同键的任务，旧任务会被取消并替换。
- **`abort`/`abort_matching`**：  
  - `abort(key)`：通过键取消任务，返回是否成功。  
  - `abort_matching(predicate)`：通过谓词匹配键并取消符合条件的任务。

### 2. **任务结果获取**
- **`join_next`**：  
  异步等待下一个完成的任务，返回 `(键, 结果)`。若无任务则返回 `None`。
- **`shutdown`**：  
  取消所有任务并等待它们完成，清空 `JoinMap`。

### 3. **状态检查**
- **`contains_key`**：检查是否存在指定键的任务。
- **`keys`**：返回所有任务键的迭代器。

---

## 工作原理
1. **任务注册**：  
   调用 `spawn` 时，任务会被添加到 `JoinSet`，同时其 `AbortHandle` 和键通过 `tasks_by_key` 和 `hashes_by_task` 记录。
2. **任务完成处理**：  
   当任务完成时，通过 `JoinSet` 获取任务 ID，利用 `hashes_by_task` 找到键的哈希值，再通过 `tasks_by_key` 确定具体键，最终返回 `(键, 结果)`。
3. **键冲突解决**：  
   `Key` 结构体通过键和任务 ID 的组合，确保哈希冲突时能正确匹配任务。

---

## 项目中的角色
`JoinMap` 是 Tokio 生态中用于**按键管理异步任务的核心工具**，提供键关联的任务取消、状态检查和结果获取功能，适用于需要灵活控制任务生命周期的场景，如分布式任务调度或键值对任务管理。
