# Tokio 运行时阻塞任务模块（mod.rs）详解

## 文件目的
该文件是 Tokio 运行时中负责管理阻塞任务的核心模块，通过抽象化阻塞线程池的集成接口，实现了以下功能：
1. 提供阻塞任务的执行环境
2. 支持条件编译（当禁用 `blocking` 特性时提供空实现）
3. 隔离线程池管理的复杂逻辑

## 关键组件

### 1. 模块与接口
```rust
mod pool;
pub(crate) use pool::{spawn_blocking, BlockingPool, Spawner};
```
- **pool 模块**：定义阻塞线程池的核心结构 `BlockingPool` 和任务调度接口
- **pub(crate) 接口**：
  - `spawn_blocking`：在阻塞线程池中执行同步阻塞任务
  - `BlockingPool`：阻塞线程池的管理结构
  - `Spawner`：任务提交接口

### 2. 特性门控接口
```rust
cfg_fs! { pub(crate) use pool::spawn_mandatory_blocking; }
cfg_trace! { pub(crate) use pool::Mandatory; }
```
- **`cfg_fs!`**：当启用文件系统特性时暴露强制阻塞接口 `spawn_mandatory_blocking`
- **`cfg_trace!`**：当启用追踪特性时暴露 `Mandatory` 类型用于标记强制阻塞任务

### 3. 线程池创建
```rust
pub(crate) fn create_blocking_pool(builder: &Builder, thread_cap: usize) -> BlockingPool {
    BlockingPool::new(builder, thread_cap)
}
```
- 根据运行时构建器（`Builder`）和线程数限制（`thread_cap`）创建阻塞线程池
- 通过 `BlockingPool::new` 初始化线程池配置

### 4. 辅助模块
```rust
mod schedule; // 任务调度策略
mod shutdown; // 线程池关闭逻辑
mod task;     // 阻塞任务结构体 `BlockingTask`
```
- **schedule**：管理任务分发和线程复用
- **shutdown**：安全终止线程池的机制
- **task**：定义 `BlockingTask` 任务结构，封装阻塞操作的执行上下文

## 工作原理
1. **任务提交**：通过 `spawn_blocking` 将阻塞任务提交到独立线程池
2. **线程管理**：线程池维持固定数量的工作线程，避免阻塞主事件循环
3. **资源控制**：通过 `thread_cap` 限制最大线程数，防止资源耗尽
4. **特性扩展**：
   - 文件系统操作等强制阻塞任务通过 `spawn_mandatory_blocking` 处理
   - 追踪特性启用时记录阻塞任务执行轨迹

## 项目中的角色