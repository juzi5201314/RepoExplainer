# `tokio/src/runtime/local_runtime/mod.rs` 文件详解

## **文件目的**
此文件是 Tokio 异步运行时的核心模块之一，负责定义和导出 **本地运行时（Local Runtime）** 的核心组件。本地运行时主要用于执行 **非 `Send` 任务**（即任务不能跨线程传递），并通过单线程调度器管理任务的执行。

---

## **关键组件**

### 1. **模块组织**
- **`mod runtime;`**: 定义本地运行时的核心逻辑，包括任务调度、生命周期管理等。
- **`mod options;`**: 提供配置本地运行时的选项（`LocalOptions`），尽管目前未定义具体配置项，但为未来扩展预留了空间（如非 `Send` 回调等）。

### 2. **导出的公共接口**
- **`pub use options::LocalOptions;`**: 导出配置本地运行时的选项结构体，允许用户自定义运行时参数。
- **`pub use runtime::LocalRuntime;`**: 导出本地运行时的核心结构体 `LocalRuntime`，用于创建和管理运行时实例。
- **`pub(super) use runtime::LocalRuntimeScheduler;`**: 仅在当前 crate 内部可见的调度器实现，负责任务的单线程调度。

---

## **核心结构体与功能**

### **`LocalRuntime`**
- **作用**：本地运行时的主入口，提供单线程任务执行环境。
- **特性**：
  - 专为 **非 `Send` 任务** 设计，确保任务仅在创建它的线程上执行。
  - 支持通过 `LocalSet` 等工具管理局部任务集合。
- **示例用法**：
  ```rust
  use tokio::runtime::LocalRuntime;
  let rt = LocalRuntime::new().unwrap();
  ```

### **`LocalOptions`**
- **作用**：配置本地运行时的参数，目前为空结构体，但预留了未来扩展的可能性（如自定义钩子或线程行为）。
- **默认配置**：直接使用 `Default` trait 创建默认实例。

---

## **与其他模块的协作**
- **`current` 模块**：提供 `with_current` 和 `try_set_current` 等函数，用于管理当前线程的运行时上下文。
- **`handle` 模块**：导出 `Handle` 和 `EnterGuard`，允许安全地访问运行时句柄并控制任务进入运行时。
- **`local` 模块**：提供 `spawn_local` 和 `LocalSet`，用于在本地运行时中创建和管理任务。
- **`task_local` 模块**：通过 `LocalKey` 实现类似 `thread_local` 的功能，支持本地任务的线程局部存储。

---

## **在项目中的角色**
此文件是 Tokio 本地运行时的核心组织模块，通过导出关键结构体和配置选项，为用户提供了创建和管理单线程本地运行时的能力，是 Tokio 支持非 `Send` 异步任务执行的重要基础设施。
