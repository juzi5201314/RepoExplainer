### 代码文件解释

#### 文件目的
该文件实现了 Tokio 异步运行时中 **禁用协作调度（coop）机制**的核心功能。通过 `unconstrained` 方法，允许特定 Future 在执行时完全不受 Tokio 协作调度策略的限制，直接控制其执行流程。

#### 关键组件

1. **`Unconstrained` 结构体**
   - 通过 `pin_project` 宏定义的 Future 封装器，包裹一个内部 Future（`inner`）。
   - `#[must_use]` 属性强制开发者必须主动轮询该 Future，否则不会触发任何操作。

2. **Future 实现**
   - **协作调度启用时** (`cfg_coop!`)：
     - 调用 `with_unconstrained` 函数包装 `inner.poll()`，标记此 Future 不参与协作调度的强制让步机制。
   - **协作调度禁用时** (`cfg_not_coop!`)：
     - 直接调用 `inner.poll()`，忽略调度策略。

3. **`unconstrained` 函数**
   - 提供统一接口创建 `Unconstrained` 实例，将用户提供的 Future 封装为不受约束的 Future。
   - 文档警告：若 Future 未自行让步，可能导致任务饥饿（starvation）。

#### 工作原理
- **协作调度机制**：Tokio 默认通过协作调度强制 Future 定期让出执行权，避免单任务独占线程。
- **禁用机制**：当 Future 被 `unconstrained` 包装后，其执行将完全由自身控制，不再受 Tokio 强制让步规则限制。
- **配置切换**：通过 `cfg_coop!` 宏实现功能开关，确保在未启用协作调度的编译配置下仍能正常工作。

#### 在项目中的角色
此文件是 Tokio 任务调度系统的重要组成部分，为开发者提供了 **绕过协作调度策略的可控手段**，在需要高性能或特定执行顺序的场景中平衡调度公平性与执行效率。
