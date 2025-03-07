# 文件说明：`tokio/src/task/builder.rs`

## **目的**  
该文件定义了 Tokio 异步运行时中任务配置的核心结构 `Builder`，用于在创建任务时设置任务属性（如名称）并选择执行方式。它是 Tokio 任务管理系统的配置入口，支持灵活控制任务的执行上下文（如线程池、本地任务集等），同时提供对阻塞代码的隔离执行能力。

---

## **关键组件**

### **1. `Builder` 结构体**
```rust
pub struct Builder<'a> {
    name: Option<&'a str>,
}
```
- **功能**：任务配置工厂，通过链式调用设置任务属性。
- **核心字段**：
  - `name`: 可选任务名称，用于调试和日志追踪。

#### **方法**
- **`new()`**: 创建默认配置的 Builder 实例。
- **`name(name: &str)`**: 配置任务名称，返回新 Builder 实例（不可变借用链式调用）。

---

### **2. 任务启动方法**
通过不同 `spawn_*` 方法启动任务，根据任务类型选择执行上下文：

#### **(1) `spawn` 和 `spawn_on`**
```rust
pub fn spawn<Fut>(self, future: Fut) -> io::Result<JoinHandle<_>>
pub fn spawn_on<Fut>(self, future: Fut, handle: &Handle)
```
- **用途**：在 Tokio 运行时中执行 `Send` 类型的异步任务。
- **特性**：
  - 检查 `future` 大小，超过阈值 `BOX_FUTURE_THRESHOLD` 时自动装箱以优化内存。
  - 通过 `SpawnMeta` 记录任务元数据（如名称），支持 Tracing 调试。

#### **(2) `spawn_local` 和 `spawn_local_on`**
```rust
pub fn spawn_local<Fut>(self, future: Fut) -> io::Result<JoinHandle<_>>
pub fn spawn_local_on<Fut>(self, future: Fut, local_set: &LocalSet)
```
- **用途**：在单线程本地任务集（`LocalSet`）中执行 `!Send` 类型的异步任务。
- **约束**：仅能在 `LocalSet` 上下文中调用。

#### **(3) `spawn_blocking` 和 `spawn_blocking_on`**
```rust
pub fn spawn_blocking<Function, Output>(self, function: Function)
pub fn spawn_blocking_on<Function, Output>(self, function: Function, handle: &Handle)
```
- **用途**：将阻塞代码提交到专用线程池执行，避免阻塞事件循环。
- **实现**：通过 `Handle` 的 `blocking_spawner` 分配任务。

---

### **3. 核心逻辑**
- **内存优化**：通过 `mem::size_of` 检测 Future 大小，超过阈值时自动装箱（`Box::pin`），平衡栈内存与堆内存的使用。
- **元数据追踪**：使用 `SpawnMeta` 记录任务名称和大小，支持 Tokio 的 Tracing 功能（如日志、性能分析）。
- **运行时集成**：通过 `Handle` 和 `LocalSet` 与 Tokio 运行时深度耦合，确保任务调度的正确性。

---

## **项目中的角色**
该文件是 Tokio 任务管理系统的核心配置组件，提供灵活的任务创建选项（如命名、执行上下文选择），并通过与运行时模块的协作，实现异步任务的高效调度和阻塞代码的隔离执行，是构建可维护异步程序的重要基础。
