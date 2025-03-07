# `tokio/src/loom/std/mutex.rs` 文件详解

## 文件目的
该文件为 Tokio 项目中的 loom 库提供了一个适配器，用于包装标准库的 `Mutex` 并去除其 **poisoning（中毒）机制**。这一设计是为了在并发测试场景中简化错误处理逻辑，确保 loom 的模拟并发测试能更灵活地控制线程行为。

---

## 核心组件

### 1. **结构体定义**
```rust
pub(crate) struct Mutex<T: ?Sized>(sync::Mutex<T>);
```
- **功能**：包装标准库的 `Mutex<T>`，通过元组结构体形式实现适配。
- **关键点**：通过隐藏原始 `Mutex` 的中毒特性，提供更简化的 API。

---

### 2. **方法实现**

#### (1) **初始化方法**
```rust
pub(crate) fn new(t: T) -> Mutex<T> {
    Mutex(sync::Mutex::new(t))
}

pub(crate) const fn const_new(t: T) -> Mutex<T> {
    Mutex(sync::Mutex::new(t))
}
```
- **功能**：提供普通和常量初始化方式，与标准库 `Mutex` 行为一致。
- **关键点**：`const_new` 允许在编译时常量上下文中创建 `Mutex`。

---

#### (2) **锁获取方法**
```rust
pub(crate) fn lock(&self) -> MutexGuard<'_, T> {
    match self.0.lock() {
        Ok(guard) => guard,
        Err(p_err) => p_err.into_inner(),
    }
}
```
- **功能**：获取锁的独占访问权。
- **关键点**：直接返回 `PoisonError` 中的值，**忽略中毒状态**，确保即使锁被毒化仍可继续使用。

---

#### (3) **非阻塞尝试获取锁**
```rust
pub(crate) fn try_lock(&self) -> Option<MutexGuard<'_, T>> {
    match self.0.try_lock() {
        Ok(guard) => Some(guard),
        Err(TryLockError::Poisoned(p_err)) => Some(p_err.into_inner()),
        Err(TryLockError::WouldBlock) => None,
    }
}
```
- **功能**：尝试立即获取锁，不阻塞线程。
- **关键点**：
  - 对 `Poisoned` 错误同样返回内部值，**消除中毒影响**。
  - 仅在锁不可用时（`WouldBlock`）返回 `None`。

---

#### (4) **可变引用获取**
```rust
pub(crate) fn get_mut(&mut self) -> &mut T {
    match self.0.get_mut() {
        Ok(val) => val,
        Err(p_err) => p_err.into_inner(),
    }
}
```
- **功能**：在独占模式下获取可变引用。
- **关键点**：同样处理 `PoisonError`，确保获取引用时不会因中毒失败。

---

## 如何融入项目
该文件属于 Tokio 的 loom 子模块，loom 是一个用于 **模拟并发执行** 的库，通过重新编译标准库来简化多线程测试。此适配器通过去除 `Mutex` 的中毒机制，确保在 loom 的测试环境中：
1. **统一错误处理**：避免因中毒导致的测试意外失败。
2. **简化逻辑**：测试代码无需额外处理中毒状态，专注于并发逻辑验证。
3. **兼容性**：提供与标准库 `Mutex` 接口一致的 API，方便在 loom 环境中无缝替换。

---

### 文件角色