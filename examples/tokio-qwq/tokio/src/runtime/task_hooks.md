# 文件说明：`task_hooks.rs`

## **文件目的**  
该文件为 Tokio 运行时提供了任务生命周期的钩子（Hooks）机制，允许用户在任务创建、终止、轮询（Poll）等关键阶段插入自定义逻辑（如监控、日志或性能分析）。通过回调函数，用户可以在不修改 Tokio 核心代码的情况下扩展运行时行为。

---

## **核心组件与功能**

### **1. `TaskHooks` 结构体**
- **作用**：管理任务事件的回调函数。
- **字段**：
  - `task_spawn_callback`: 任务创建时触发的回调。
  - `task_terminate_callback`: 任务终止时触发的回调。
  - `[cfg(tokio_unstable)] before_poll_callback`: 轮询开始前触发的回调（实验性功能）。
  - `[cfg(tokio_unstable)] after_poll_callback`: 轮询结束后触发的回调（实验性功能）。

### **2. `TaskMeta` 结构体**
- **作用**：提供任务元数据（如任务 ID），在回调中传递给用户。
- **字段**：
  - `id`: 任务的唯一标识符。
  - `_phantom`: 生命周期标记，确保泛型安全。

### **3. 回调函数类型 `TaskCallback`**
- **定义**：`Arc<dyn Fn(&TaskMeta<'_>) + Send + Sync>`。
- **特性**：  
  - 使用 `Arc` 实现共享所有权。
  - 要求回调函数是线程安全的（`Send + Sync`）。

---

## **关键方法实现**

### **`TaskHooks` 方法**
#### **`spawn(&self, meta: &TaskMeta<'_>)`**
- **触发时机**：任务创建时。
- **行为**：若 `task_spawn_callback` 存在，则调用该回调，传递 `TaskMeta`。

#### **`from_config(config: &Config) -> Self`**
- **作用**：从配置对象 `Config` 初始化 `TaskHooks`，将配置中的回调复制到结构体字段中。

#### **`poll_start_callback` 和 `poll_stop_callback`**
- **触发时机**：任务轮询（Poll）开始/结束时（需启用 `tokio_unstable` 特性）。
- **行为**：若对应回调存在，则调用并传递任务元数据。

---

## **与项目其他部分的关联**
1. **配置集成**：通过 `Config` 结构体传递用户定义的回调，实现钩子的可配置性。
2. **任务生命周期管理**：钩子函数在任务创建、终止及轮询阶段被 Tokio 内部调度器调用，例如：
   - 任务创建时调用 `spawn`。
   - 轮询开始前调用 `poll_start_callback`。
3. **实验性功能**：`before_poll` 和 `after_poll` 钩子标记为不稳定（`tokio_unstable`），表明其 API 可能随版本变化。

---

## **文件在项目中的角色**