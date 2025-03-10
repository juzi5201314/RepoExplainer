### 文件说明：Tokio运行时任务核心模块

#### 目的
该文件是Tokio异步运行时的核心组件，负责定义任务（Task）的底层结构和生命周期管理。通过精心设计的内存布局和线程安全机制，实现高效的任务调度和执行。

#### 关键组件

1. **任务结构体 `Cell<T, S>`**
   - **Header**（热数据）：
     - `State`：任务状态（就绪、运行中、完成等）
     - `queue_next`：任务队列指针（用于调度队列）
     - `vtable`：虚函数表（存储任务操作的函数指针）
     - `owner_id`：任务所属调度器的标识
   - **Core**（核心数据）：
     - `scheduler`：任务调度器
     - `task_id`：唯一任务ID
     - `stage`：任务阶段（运行态/完成态/已消费）
   - **Trailer**（冷数据）：
     - `owned`：任务在调度器列表中的指针
     - `waker`：唤醒器（用于任务间协作）
     - `hooks`：调度钩子函数

2. **内存布局优化**
   - 通过 `repr(align(N))` 对齐到CPU缓存行大小（根据架构不同为16/32/64/128/256字节）
   - `Header` 作为首个字段确保指针兼容性
   - 热数据（Header/Core）与冷数据（Trailer）分离，减少缓存污染

3. **任务生命周期管理**
   - `poll()` 方法驱动Future执行，通过 `TaskIdGuard` 管理当前任务ID
   - `store_output()` 和 `take_output()` 处理任务结果的存储与释放
   - `drop_future_or_output()` 确保资源安全释放

4. **并发安全机制**
   - 广泛使用 `UnsafeCell` 实现无锁并发访问
   - 通过 `vtable` 提供类型安全的虚函数调用
   - `owner_id` 确保任务仅在所属调度器中操作

#### 工作原理
1. **任务创建**：
   - `Cell::new()` 初始化任务结构，设置调度器、初始状态和ID
   - 通过 `vtable` 预置任务操作函数指针

2. **任务执行**：
   - 调度器通过 `poll()` 方法轮询Future
   - `TaskIdGuard` 动态设置当前任务ID，支持错误追踪

3. **状态转换**：
   - `Stage` 枚举管理任务生命周期阶段（运行态→完成态→已消费态）
   - 状态变更需通过 `unsafe` 方法确保线程安全

4. **调度协作**：
   - `Trailer` 中的 `waker` 实现任务间唤醒
   - `owned` 指针管理任务在调度器队列中的位置

#### 项目中的角色
该文件是Tokio运行时任务系统的基石，定义了任务的核心数据结构和操作接口，通过高效的内存布局和并发控制机制，为异步任务的创建、调度和执行提供底层支持，是运行时性能和可靠性的关键实现组件。
