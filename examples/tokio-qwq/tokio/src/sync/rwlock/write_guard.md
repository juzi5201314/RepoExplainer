# RwLockWriteGuard 结构体详解

## 文件目的
该文件实现了 Tokio 异步 RwLock 的写锁持有者（Write Guard）功能。通过 RAII 模式管理互斥锁的独占访问权限，确保锁在作用域结束时自动释放。同时提供数据映射和锁降级等高级功能，支持安全地操作共享资源。

---

## 核心组件

### 1. **结构体定义**
```rust
pub struct RwLockWriteGuard<'a, T: ?Sized> {
    // ...（字段说明见下方）
}
```
- **关键字段**：
  - `permits_acquired`: 获取的信号量许可数，用于控制锁的持有状态
  - `s`: 内部使用的信号量（Semaphore），管理锁的访问权限
  - `data`: 指向被锁定数据的原始指针
  - `resource_span`(可选): 跟踪锁状态的 tracing 调用链（需启用 `tracing` 功能）

---

### 2. **核心方法**

#### **锁映射操作**
- **`map` 方法**
  ```rust
  pub fn map<F, U: ?Sized>(mut this: Self, f: F) -> RwLockMappedWriteGuard<'a, U>
  ```
  将当前锁持有的数据映射到其子组件，返回新的 `RwLockMappedWriteGuard`。例如：
  ```rust
  let mut mapped = RwLockWriteGuard::map(lock.write().await, |f| &mut f.0);
  ```

- **`downgrade_map` 方法**
  ```rust
  pub fn downgrade_map<F, U: ?Sized>(this: Self, f: F) -> RwLockReadGuard<'a, U>
  ```
  将写锁降级为读锁并映射到指定组件。会释放多余的许可，仅保留一个写锁权限：
  ```rust
  let mapped = RwLockWriteGuard::downgrade_map(lock.write().await, |f| &f.0);
  ```

#### **锁降级**
- **`downgrade` 方法**
  ```rust
  pub fn downgrade(self) -> RwLockReadGuard<'a, T>
  ```
  将独占写锁安全降级为共享读锁，确保降级过程中不会被其他写者抢占：
  ```rust
  let n = n.downgrade(); // 写锁 → 读锁
  ```

#### **错误处理**
- **`try_map` 和 `try_downgrade_map`**
  提供可失败的映射/降级操作，当闭包返回 `None` 时保留原锁：
  ```rust
  let guard = RwLockWriteGuard::try_map(guard, |f| Some(&mut f.0)).expect("...");
  ```

---

### 3. **自动解引用**
```rust
impl<T: ?Sized> ops::DerefMut for RwLockWriteGuard<'_, T> {
    fn deref_mut(&mut self) -> &mut T { unsafe { &mut *self.data } }
}
```
通过 `Deref` 和 `DerefMut` 允许直接使用 `*guard` 访问数据，隐藏底层指针操作。

---

### 4. **资源释放**
```rust
impl<'a, T: ?Sized> Drop for RwLockWriteGuard<'a, T> {
    fn drop(&mut self) {
        self.s.release(self.permits_acquired as usize);
        // ... tracing 日志（可选）
    }
}
```
在作用域结束时自动释放所有持有的信号量许可，确保锁正确解锁。

---

## 项目中的角色