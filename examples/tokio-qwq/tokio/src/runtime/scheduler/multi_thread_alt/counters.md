### 代码文件解释

#### 目的
该文件是 Tokio 运行时多线程调度器的计数器模块，用于统计调度器在运行过程中各种操作的执行次数。通过启用 `tokio_internal_mt_counters` 特性，可以收集关键操作的统计信息，帮助调试和性能分析。

#### 关键组件
1. **原子计数器（Atomic Counters）**
   - 使用 `AtomicUsize` 类型定义了一系列静态变量（如 `NUM_MAINTENANCE`, `NUM_NOTIFY_LOCAL` 等），用于记录以下操作的次数：
     - 维护任务（`maintenance`）
     - 本地/远程通知（`notify`）
     - 本地/远程唤醒（`unparks`）
     - LIFO 调度和队列溢出（`LIFO schedules`, `overflow`）
     - 任务窃取（`steals`）
     - 全局队列访问（`global queue interval`）
     - 线程空闲或无任务的情况（`no local work`, `no core`）

2. **Drop 实现**
   - 当 `Counters` 实例被销毁时，会触发 `drop` 方法，将所有计数器的值格式化输出到控制台。例如：
     ```text
     notifies (remote): 123
     unparks (local): 456
     maintenance: 789
     ...
     ```

3. **计数器递增函数**
   - 提供了一系列 `inc_num_*` 函数（如 `inc_num_notify_local`），用于在对应操作发生时原子地增加计数器的值。例如：
     ```rust
     pub(crate) fn inc_num_notify_remote() {
         NUM_NOTIFY_REMOTE.fetch_add(1, Relaxed);
     }
     ```

4. **条件编译（Conditional Compilation）**
   - 当禁用 `tokio_internal_mt_counters` 特性时，所有计数器函数被空实现（`no-op`），避免不必要的性能开销。

#### 作用与集成
- **统计信息收集**：在启用特性时，调度器的各个组件（如线程池、任务队列）通过调用 `inc_num_*` 函数记录操作次数。
- **调试与优化**：通过输出的统计信息，开发者可以分析任务调度的热点、线程利用率、任务窃取频率等问题，进而优化调度算法。
- **零开销抽象**：通过条件编译，在禁用特性时完全移除计数器逻辑，确保生产环境下的性能无损耗。

#### 项目中的角色
此文件为 Tokio 多线程调度器提供了可选的统计计数功能，帮助开发者监控和优化任务调度的性能表现。
