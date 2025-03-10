### 文件说明：`tokio/src/runtime/scheduler/current_thread/mod.rs`

#### **文件目的**
该文件是 Tokio 异步运行时中 **单线程调度器**的核心实现，负责在当前线程上执行任务队列，管理任务调度、资源驱动（如 I/O 和计时器）以及线程阻塞/唤醒逻辑。它是单线程运行时（如 `Runtime::new()`）的核心组件，确保任务在单一线程上高效执行。

---

#### **关键组件**

1. **`CurrentThread` 结构体**
   - **作用**：调度器的核心管理器，维护任务队列和运行时状态。
   - **核心字段**：
     - `core`: 使用 `AtomicCell` 包装的调度器核心数据，通过 `block_on` 方法获取。
     - `notify`: 用于线程间通知的 `Notify` 实例，协调任务唤醒。
   - **方法**：
     - `new()`: 初始化调度器，配置驱动、任务队列和指标。
     - `block_on()`: 驱动 Future 执行至完成，处理任务调度和线程阻塞。
     - `shutdown()`: 关闭运行时，清理任务和资源。

2. **`Handle` 结构体**
   - **作用**：提供对调度器状态的访问，包括驱动、阻塞池、配置和任务钩子。
   - **核心字段**：
     - `shared`: 共享状态（如任务队列、配置和指标）。
     - `driver`: 资源驱动句柄，管理 I/O 和计时器事件。
   - **方法**：
     - `spawn()`: 在单线程调度器上启动新任务。
     - `schedule()`: 将任务加入调度队列。
     - `wake_by_ref()`: 唤醒线程以处理新任务。

3. **`Core` 结构体**
   - **作用**：包含调度器的实际运行数据，如任务队列、计时器和指标。
   - **核心字段**：
     - `tasks`: 本地任务队列（`VecDeque`）。
     - `driver`: 资源驱动实例，处理 I/O 和计时器事件。
   - **方法**：
     - `next_task()`: 根据策略选择下一个执行的任务。
     - `park()`: 阻塞线程直到有新事件或任务。
     - `submit_metrics()`: 提交运行时指标数据。

4. **`Context` 结构体**
   - **作用**：线程局部上下文，保存 `Core` 和延迟任务队列。
   - **核心方法**：
     - `run_task()`: 在上下文中执行任务并跟踪执行预算。
     - `defer()`: 将需要让步的任务加入延迟队列。

---

#### **核心逻辑流程**

1. **任务调度**
   - **本地优先策略**：优先从本地队列 (`tasks`) 获取任务，每隔固定间隔 (`global_queue_interval`) 检查全局队列。
   - **任务唤醒**：通过 `Notify` 实现线程间协作，确保新任务或事件触发时线程及时响应。

2. **阻塞与唤醒**
   - **`park()` 方法**：当任务队列为空时，线程阻塞等待事件（如 I/O 完成或定时器触发）。
   - **`unpark()`**：通过 `driver.unpark()` 唤醒阻塞线程，处理新事件或任务。

3. **任务执行循环**
   - **`block_on` 内部循环**：
     1. 持续从任务队列中获取任务并执行。
     2. 定期检查全局队列，避免饥饿。
     3. 当队列为空时，调用 `park()` 阻塞线程，直到有新事件。

4. **资源管理**
   - **驱动集成**：通过 `Driver` 管理 I/O 和计时器事件，确保异步操作的正确触发。
   - **指标收集**：记录任务调度次数、队列深度等，用于性能监控。

---

#### **与项目其他部分的关联**
- **依赖关系**：
  - `driver`: 管理 I/O 和计时器事件。
  - `task`: 定义任务结构和生命周期。
  - `metrics`: 收集运行时性能数据。
- **集成点**：
  - 通过 `Handle` 提供对外接口，支持任务启动和配置。
  - 与 `Runtime` 类型协作，作为单线程运行时的核心调度器。

---

#### **文件在项目中的角色**