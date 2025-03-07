# 文件解释：`tokio/src/runtime/scheduler/mod.rs`

## 文件目的
该文件是Tokio运行时调度器的核心模块，负责管理不同调度策略的抽象与实现。根据编译时配置（单线程或多线程模式），提供统一的接口来协调任务调度、执行和资源管理。

---

## 关键组件

### 1. **条件编译模块**
通过`cfg_rt!`和`cfg_rt_multi_thread!`宏根据功能开关动态包含模块：
- **单线程模式（`feature = "rt"`）**：
  - 引入`current_thread`模块，实现单线程调度器
  - 包含`defer`和`inject`模块，用于任务延迟执行和注入
- **多线程模式（`feature = "rt-multi-thread"`）**：
  - 引入`multi_thread`模块，实现多线程调度器
  - 实验性`multi_thread_alt`模块（需`tokio_unstable`开关）
  - 包含`block_in_place`和`lock`模块处理阻塞操作和锁机制

---

### 2. **核心结构：`Handle`枚举**
统一调度器接口的抽象层，根据运行时类型持有不同调度器的句柄：
```rust
pub(crate) enum Handle {
    CurrentThread(Arc<current_thread::Handle>),      // 单线程模式
    MultiThread(Arc<multi_thread::Handle>),          // 标准多线程模式
    MultiThreadAlt(Arc<multi_thread_alt::Handle>),   // 实验性多线程模式
    Disabled,                                       // 无运行时时的占位
}
```
- **功能方法**：
  - `driver()`: 获取底层驱动句柄
  - `spawn()`: 根据运行时类型分发任务创建
  - `shutdown()`: 关闭调度器
  - `num_workers()`: 返回工作线程数量（多线程模式）
  - `spawn_local()`: 安全创建本地任务（仅单线程模式）

---

### 3. **上下文结构：`Context`枚举**
表示运行时的执行上下文，用于调度器内部状态管理：
```rust
pub(super) enum Context {
    CurrentThread(current_thread::Context),
    MultiThread(multi_thread::Context),
    MultiThreadAlt(multi_thread_alt::Context),
}
```
- **关键方法**：
  - `defer()`: 延迟唤醒任务
  - `expect_*()`: 类型断言方法，确保上下文类型匹配

---

### 4. **调度策略实现**
- **单线程调度器**：
  - 通过`current_thread::Handle`管理单线程任务队列
  - 支持本地任务（`spawn_local`）
- **多线程调度器**：
  - `multi_thread`模块实现工作线程池管理
  - `multi_thread_alt`为实验性优化实现
- **阻塞操作处理**：
  - `block_in_place`模块隔离阻塞代码，避免影响事件循环

---

### 5. **扩展功能**
- **统计指标（Metrics）**：
  - 当启用`unstable_metrics`时，提供任务计数、队列深度等监控数据
- **跨平台兼容性**：
  - 通过条件编译处理不同平台的依赖（如`net`、`process`等）

---

## 文件在项目中的角色
作为Tokio运行时的核心调度模块，该文件通过抽象不同调度策略（单线程/多线程），提供统一的API接口，协调任务调度、资源管理和执行上下文。它是运行时与具体调度实现之间的桥梁，确保用户代码无需关心底层调度细节，即可高效运行异步任务。
