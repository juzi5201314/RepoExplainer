### 文件说明：`tokio/src/sync/rwlock/owned_read_guard.rs`

#### 目的
该文件实现了 Tokio 的 `OwnedRwLockReadGuard` 结构体，用于管理对 `RwLock` 的独占读访问。通过 RAII（资源获取即初始化）模式确保在离开作用域时自动释放锁，避免死锁或资源泄漏。

---

#### 关键组件

1. **结构体定义**
   ```rust
   pub struct OwnedRwLockReadGuard<T: ?Sized, U: ?Sized = T> {
       #[cfg(all(tokio_unstable, feature = "tracing"))]
       pub(super) resource_span: tracing::Span,
       pub(super) lock: Arc<RwLock<T>>,
       pub(super) data: *const U,
       pub(super) _p: PhantomData<T>,
   }
   ```
   - **`lock`**: 持有 `RwLock` 的 `Arc` 引用，确保多个 `OwnedRwLockReadGuard` 可以安全共享同一个锁。
   - **`data`**: 指向被锁定数据的原始指针，通过 `Deref` trait 提供安全的解引用访问。
   - **`resource_span`**: 可选的追踪功能（需启用 `tokio_unstable` 和 `tracing` 特性），用于记录锁的使用状态。
   - **`_p`**: `PhantomData` 用于标记生命周期和类型参数，确保类型系统正确性。

2. **核心方法**
   - **`skip_drop`**:
     ```rust
     fn skip_drop(self) -> Inner<T, U> { /* ... */ }
     ```
     在转移所有权时避免触发 `Drop`，通过 `mem::ManuallyDrop` 和指针操作安全地复制字段。

   - **`map` 和 `try_map`**:
     ```rust
     pub fn map<F, V: ?Sized>(this: Self, f: F) -> OwnedRwLockReadGuard<T, V> { /* ... */ }
     ```
     允许将锁持有的数据映射到其子部分（如结构体字段），返回新 `OwnedRwLockReadGuard` 实例，同时保持锁的有效性。`try_map` 在映射失败时返回原始 guard。

   - **`rwlock`**:
     ```rust
     pub fn rwlock(this: &Self) -> &Arc<RwLock<T>> { &this.lock }
     ```
     获取原始 `RwLock` 的引用，用于调试或进一步操作。

3. **Trait 实现**
   - **`Deref`**:
     ```rust
     impl<T: ?Sized, U: ?Sized> ops::Deref for OwnedRwLockReadGuard<T, U> { /* ... */ }
     ```
     通过 `*guard` 直接访问被锁定的数据，确保语法简洁安全。

   - **`Drop`**:
     ```rust
     fn drop(&mut self) {
         self.lock.s.release(1);
         // 可选的追踪记录
     }
     ```
     在 guard 被销毁时释放读锁，通过调用 `release(1)` 减少读锁计数。若启用了追踪功能，会记录锁状态变化。

---

#### 在项目中的角色
该文件是 Tokio 异步运行时中 `RwLock` 机制的核心组件之一，提供以下功能：
- **安全的读锁持有**：通过 RAII 确保锁在作用域结束时自动释放。
- **数据映射支持**：允许在不释放锁的情况下访问数据的子部分，提升灵活性。
- **性能与调试**：通过 `Arc` 实现共享，结合可选的追踪功能辅助性能分析。
