# `tokio/src/loom/std/atomic_u64.rs` 文件详解

## 文件目的
该文件为 Tokio 的 loom 库提供跨平台的原子 `u64` 类型实现。其核心目标是通过条件编译适配不同平台特性：
- **64位平台**：直接使用标准库的 `AtomicU64` 实现高效原子操作
- **32位或不支持原子64位操作的平台**：通过 `Mutex` 模拟原子性，确保兼容性

## 关键组件

### 1. 条件编译模块导入
```rust
cfg_has_atomic_u64! { mod imp; } // 导入 native 实现
cfg_not_has_atomic_u64! { mod imp; } // 导入 mutex 实现
```
- 使用自定义宏 `cfg_has_atomic_u64!` 和 `cfg_not_has_atomic_u64!` 进行平台检测
- 根据目标平台特性选择性编译：
  - `atomic_u64_native.rs`（原生支持原子操作）
  - `atomic_u64_as_mutex.rs`（使用互斥锁模拟）

### 2. 公开接口
```rust
pub(crate) use imp::{AtomicU64, StaticAtomicU64};
```
- 向 Tokio 内部暴露两个类型：
  - `AtomicU64`：线程安全的原子 `u64` 类型
  - `StaticAtomicU64`：用于静态初始化的原子类型（可能包含延迟初始化逻辑）

### 3. 32位平台实现（来自 `atomic_u64_as_mutex.rs`）
```rust
pub(crate) struct AtomicU64 {
    inner: Mutex<u64>,
}
```
- 使用 `Mutex` 包裹 `u64` 实现原子操作
- 所有操作（如读写）需通过锁的保护，确保线程安全
- `StaticAtomicU64` 可能包含 `OnceCell` 用于延迟初始化：
  ```rust
  pub(crate) struct StaticAtomicU64 {
      init: u64,
      cell: OnceCell<Mutex<u64>>,
  }
  ```

### 4. 兼容性注释
- 提到未来计划使用稳定 Rust 特性 `#[cfg(target_has_atomic = "64")]` 替代当前宏
- 说明当前依赖 `cfg_has_atomic_u64!` 等自定义宏处理平台检测

## 在项目中的角色
该文件是 Tokio 并发基础组件的一部分，通过智能适配不同平台特性，为 loom 的并发测试框架提供可靠的原子操作支持，确保 Tokio 在不同硬件架构上的正确性和性能表现。
