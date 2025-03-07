# 文件说明：`tokio-util/src/time/wheel/stack.rs`

## 文件目的
此文件定义了时间轮（time wheel）中用于管理超时任务的栈操作抽象接口 `Stack`。通过提供统一的栈操作规范，该 trait 支持时间轮高效管理定时任务的到期事件。

## 核心组件与功能

### 核心 Trait：`Stack`
```rust
pub(crate) trait Stack: Default {
    // 关联类型定义
    type Owned: Borrow<Self::Borrowed>;
    type Borrowed: Eq + Hash;
    type Store;

    // 栈操作方法
    fn is_empty(&self) -> bool;
    fn push(&mut self, item: Self::Owned, store: &mut Self::Store);
    fn pop(&mut self, store: &mut Self::Store) -> Option<Self::Owned>;
    fn peek(&self) -> Option<Self::Owned>;
    fn remove(&mut self, item: &Self::Borrowed, store: &mut Self::Store);
    fn when(item: &Self::Borrowed, store: &Self::Store) -> u64;
}
```

#### 关联类型说明：
1. **`Owned`**  
   栈中存储的项的所有权类型，需实现对 `Borrowed` 的借用能力（通过 `Borrow` trait）。
   
2. **`Borrowed`**  
   可借用的项类型，必须实现 `Eq` 和 `Hash`，用于哈希表等数据结构的键比较。

3. **`Store`**  
   存储项的具体实现类型（如 `SlabStorage`），允许使用内存池（slab）替代堆分配以优化性能。

#### 核心方法：
- **`is_empty`**：检查栈是否为空。
- **`push`**：将项压入栈，需配合 `Store` 管理内存。
- **`pop`**：弹出栈顶元素，返回所有权。
- **`peek`**：查看栈顶元素但不移除。
- **`remove`**：根据键移除特定项。
- **`when`**：获取项的到期时间（`u64` 类型的时间戳）。

### 实现细节（通过上下文推断）：
1. **存储优化**  
   使用 `SlabStorage` 等内存池技术替代堆分配，减少内存碎片和分配开销。

2. **安全性校验**  
   在 `push` 方法中通过 `debug_assert` 确保项未被重复插入栈。

3. **状态管理**  
   `clear` 方法用于重置栈状态，清空存储并重置时间轮相关结构（如 `expired` 栈和 `wheel`）。

## 在项目中的角色
此文件为 Tokio 时间轮提供了**栈操作的抽象接口**，是时间轮管理超时任务的核心组件。通过定义统一的栈操作规范，它支持时间轮高效轮询到期任务，并通过内存池优化实现低开销的定时任务调度。
