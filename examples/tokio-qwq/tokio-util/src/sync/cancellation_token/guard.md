rust
use crate::sync::CancellationToken;

/// A wrapper for cancellation token which automatically cancels it on drop.  
/// It is created using `drop_guard` method on the `CancellationToken`.  
#[derive(Debug)]
pub struct DropGuard {
    pub(super) inner: Option<CancellationToken>,
}

impl DropGuard {
    /// Returns stored cancellation token and removes this drop guard instance  
    /// (i.e. it will no longer cancel token). Other guards for this token are not affected.  
    pub fn disarm(mut self) -> CancellationToken {
        self.inner
            .take()
            .expect("`inner` can be only None in a destructor")
    }
}

impl Drop for DropGuard {
    fn drop(&mut self) {
        if let Some(inner) = &self.inner {
            inner.cancel();
        }
    }
}
```

### 代码文件解释

#### **功能与目的**
该文件定义了一个名为 `DropGuard` 的结构体，用于自动管理 `CancellationToken` 的生命周期。其核心作用是：当 `DropGuard` 实例被销毁时，会自动触发关联的 `CancellationToken` 的取消操作。这种机制通过 RAII（资源获取即初始化）模式实现，确保在作用域结束时自动执行清理操作。

#### **关键组件**
1. **结构体 `DropGuard`**
   - **字段 `inner`**：类型为 `Option<CancellationToken>`，用于存储关联的取消令牌。使用 `Option` 是为了在 `DropGuard` 被 `disarm` 方法解除武装时，能够安全地取出内部值。
   - **派生 `Debug` 特征**：允许通过 `println!("{:?}")` 等方式打印调试信息。

2. **方法 `disarm`**
   - **功能**：将内部的 `CancellationToken` 取出并返回，同时使当前 `DropGuard` 失效（不再触发取消操作）。此操作不会影响其他可能存在的 `DropGuard` 实例。
   - **实现**：通过 `take()` 方法消耗 `self` 并取出内部值，确保 `DropGuard` 在后续生命周期中不再执行取消操作。

3. **`Drop` 特征实现**
   - **触发条件**：当 `DropGuard` 实例超出作用域或被显式丢弃时自动调用。
   - **行为**：检查 `inner` 是否存在，若存在则调用其 `cancel()` 方法，触发关联的取消操作。

#### **与其他组件的交互**
- **`CancellationToken` 的 `drop_guard` 方法**：该方法会创建 `DropGuard` 实例，并将其与某个 `CancellationToken` 关联。例如：
  ```rust
  let token = CancellationToken::new();
  let guard = token.drop_guard(); // 创建 DropGuard
  // 当 guard 超出作用域时，token 将被自动取消
  ```
- **取消机制**：当 `DropGuard` 被销毁时，会通过 `inner.cancel()` 触发关联的 `CancellationToken` 的取消状态，通知所有等待该令牌的异步任务终止。

#### **项目中的角色**
该文件是 Tokio 取消机制的核心组件之一，通过 `DropGuard` 提供了自动化的取消触发能力，确保在作用域结束时安全地取消异步操作，避免资源泄漏或未预期的阻塞。它与 `CancellationToken` 共同构成了 Tokio 中用于协调异步任务取消的同步原语。
