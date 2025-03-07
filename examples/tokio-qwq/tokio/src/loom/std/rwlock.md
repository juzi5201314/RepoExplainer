# 文件说明：tokio/src/loom/std/rwlock.rs

## 文件目的
该文件为 Tokio 项目中的 loom 模块提供了一个适配器，用于去除标准库 `std::sync::RwLock` 的"锁中毒（poisoning）"特性。通过消除锁中毒机制，该实现能够更灵活地支持并发测试场景下的锁操作。

## 核心组件

### 1. RwLock 结构体
```rust
pub(crate) struct RwLock<T: ?Sized>(sync::RwLock<T>);
```
- **功能**：包装标准库的 RwLock，隐藏其中毒特性
- **特性**：
  - 使用 `pub(crate)` 限制作用域，仅在当前 crate 内可见
  - 通过元组结构体直接封装原始 RwLock 实例

### 2. 构造方法
```rust
pub(crate) fn new(t: T) -> Self {
    Self(sync::RwLock::new(t))
}
```
- 提供与标准库一致的构造接口，初始化内部 RwLock 实例

### 3. 读锁操作
```rust
pub(crate) fn read(&self) -> RwLockReadGuard<'_, T> {
    match self.0.read() {
        Ok(guard) => guard,
        Err(p_err) => p_err.into_inner(),
    }
}
```
- **关键逻辑**：
  - 直接返回锁的 guard，无论是否发生中毒
  - 当锁中毒时（`Err`），通过 `into_inner()` 获取内部 guard
- `try_read()` 方法实现类似，但返回 `Option` 类型

### 4. 写锁操作
```rust
pub(crate) fn write(&self) -> RwLockWriteGuard<'_, T> {
    match self.0.write() {
        Ok(guard) => guard,
        Err(p_err) => p_err.into_inner(),
    }
}
```
- 写锁操作同样忽略中毒状态，强制返回 guard
- `try_write()` 方法实现类似，支持非阻塞尝试获取

## 实现机制
- **中毒机制消除**：通过处理 `PoisonError` 的 `into_inner()` 方法，直接获取内部 guard，跳过标准库的中毒检查
- **错误处理策略**：
  - 对于 `PoisonError`：直接返回内部 guard（视为未中毒）
  - 对于 `WouldBlock`：返回 `None`（仅在 `try_` 方法中）
- **生命周期管理**：通过标准库的 guard 类型保持内存安全

## 项目中的角色
该文件为 Tokio 的 loom 并发测试框架提供定制化的 RwLock 实现，通过消除锁中毒特性，确保测试场景中锁操作的可预测性和稳定性，便于开发者更有效地验证并发模型的正确性。
