# 文件说明：`merge.rs`

## 文件目的  
该文件实现了 Tokio 流（Stream）的 `merge` 方法，用于将两个流合并为一个流。合并后的流会交替轮询两个原始流，按顺序返回它们的元素，直到两个流都完成。

---

## 核心组件与实现细节  

### 1. `Merge` 结构体  
```rust
pin_project! {
    pub struct Merge<T, U> {
        #[pin] a: Fuse<T>,
        #[pin] b: Fuse<U>,
        a_first: bool,
    }
}
```  
- **字段说明**：  
  - `a` 和 `b`：通过 `Fuse` 包装的原始流，确保流完成（`poll_next` 返回 `None`）后不再被轮询。  
  - `a_first`：布尔标志，控制每次轮询时优先检查哪个流（`true` 表示先轮询 `a`，否则先轮询 `b`）。  

- **初始化**：  
  `new` 方法通过 `Fuse::new` 初始化两个流，并设置初始轮询顺序为 `a_first = true`。

---

### 2. `Stream` 特性实现  
```rust
impl<T, U> Stream for Merge<T, U> { ... }
```  
- **`poll_next` 方法**：  
  - 每次调用时切换 `a_first` 标志，确保交替轮询 `a` 和 `b`。  
  - 调用辅助函数 `poll_next`，优先轮询第一个流（根据 `a_first` 决定是 `a` 还是 `b`），若未获取到元素则轮询第二个流。  
  - 若两个流均完成（`Poll::Ready(None)`），则返回 `None`。  

- **`size_hint` 方法**：  
  调用 `merge_size_hints` 合并两个流的大小提示（最小和最大可能元素数）。

---

### 3. 辅助函数 `poll_next`  
```rust
fn poll_next<T, U>(first: Pin<&mut T>, second: Pin<&mut U>, cx: &mut Context<'_>) -> Poll<Option<T::Item>> { ... }
```  
- **逻辑流程**：  
  1. 先轮询 `first` 流：  
     - 若返回元素，直接返回该元素。  
     - 若流已完成（`Ready(None)`），跳过。  
     - 若流未就绪（`Pending`），标记 `done = false`。  
  2. 再轮询 `second` 流，逻辑同上。  
  3. 若两个流均完成（`done` 为 `true`），返回 `Ready(None)`；否则返回 `Pending`。

---

## 与其他组件的关联  
- **`Fuse` 结构体**：来自 `crate::stream_ext::Fuse`，用于标记流是否已完成，避免重复轮询空流。  
- **`merge_size_hints`**：在 `super` 模块中定义，合并两个流的 `size_hint`。  
- **轮询策略**：通过交替轮询 `a` 和 `b`，确保两个流公平竞争，避免某一流被长期阻塞。

---

## 在项目中的角色  
该文件实现了 Tokio 流的 `merge` 功能，允许开发者将两个流合并为一个流，按交替顺序处理元素，是 Tokio 异步流处理的核心工具之一。  