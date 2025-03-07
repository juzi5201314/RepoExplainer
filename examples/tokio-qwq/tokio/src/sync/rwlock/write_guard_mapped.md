### 代码文件说明

#### 文件目的
该文件实现了 Tokio 异步 RwLock 的写锁映射机制（`RwLockMappedWriteGuard`），用于在保持写锁独占访问的同时，安全地将锁持有的数据映射到其内部组件。通过提供 `map` 和 `try_map` 方法，允许用户在不释放锁的情况下操作数据的子部分，同时确保线程安全和资源正确释放。

---

#### 核心组件

1. **结构体定义**
   ```rust
   pub struct RwLockMappedWriteGuard<'a, T: ?Sized> { ... }
   ```
   - **字段说明**：
     - `permits_acquired`: 记录当前持有的许可数（通过信号量管理）。
     - `s`: 指向控制锁的 `Semaphore` 实例。
     - `data`: 数据的可变指针，指向实际被锁保护的资源。
     - `resource_span`: 可选的追踪信息（当启用 `tracing` 特性时）。
     - `marker`: 生命周期标记，确保类型安全。

2. **`skip_drop` 方法**
   ```rust
   fn skip_drop(self) -> Inner<'a, T> { ... }
   ```
   - 用于在 `map` 和 `try_map` 中安全地转移字段所有权，避免重复释放资源。

3. **映射方法**
   - **`map` 方法**
     ```rust
     pub fn map<F, U: ?Sized>(mut this: Self, f: F) -> RwLockMappedWriteGuard<'a, U> { ... }
     ```
     - 接受闭包 `f`，将当前锁持有的数据映射到其组件（如结构体字段），返回新 Guard。
     - 示例：将 `RwLock<Foo>` 的写锁映射为 `RwLockMappedWriteGuard<u32>`，直接操作 `Foo` 的 `u32` 字段。

   - **`try_map` 方法**
     ```rust
     pub fn try_map<F, U: ?Sized>(mut this: Self, f: F) -> Result<..., Self> { ... }
     ```
     - 类似 `map`，但闭包返回 `Option`，失败时返回原 Guard。

4. **Deref/DerefMut 实现**
   ```rust
   impl<T: ?Sized> ops::DerefMut for RwLockMappedWriteGuard<'_, T> { ... }
   ```
   - 允许通过 `*guard` 直接访问数据，简化语法。

5. **Drop 实现**
   ```rust
   impl<'a, T: ?Sized> Drop for RwLockMappedWriteGuard<'a, T> { ... }
   ```
   - 释放信号量许可，确保锁正确解锁。
   - 若启用追踪功能，记录锁释放事件。

---

#### 关键特性
- **禁止降级**：注释明确说明不允许通过 `downgrade` 方法降级为读锁，因为映射操作可能破坏锁的内部一致性。
- **异步兼容性**：基于 `batch_semaphore` 实现，与 Tokio 的异步任务调度无缝集成。
- **类型安全**：通过 `PhantomData` 和生命周期标记确保借用检查器的安全性。

---

#### 在项目中的角色