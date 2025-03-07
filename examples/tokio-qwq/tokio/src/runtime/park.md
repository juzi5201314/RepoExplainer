### 文件说明：tokio/src/runtime/park.rs

#### 文件目的
该文件实现了 Tokio 运行时中线程的阻塞（park）和唤醒（unpark）机制，是异步任务调度的核心组件。通过原子操作、条件变量和互斥锁的组合，管理线程的阻塞状态和唤醒逻辑，确保线程在无任务时高效休眠，并在事件触发时快速恢复执行。

---

#### 关键组件

1. **核心结构**
   - **ParkThread**  
     表示当前线程的阻塞句柄，包含指向 `Inner` 的 `Arc`。提供 `park()` 和 `park_timeout()` 方法阻塞当前线程，并通过 `unpark()` 方法生成唤醒句柄。
   - **UnparkThread**  
     唤醒句柄，通过 `unpark()` 方法唤醒被阻塞的线程。可跨线程克隆，支持多线程协作唤醒。
   - **Inner**  
     内部状态管理结构，包含：
     - `state`: 原子状态标志（EMPTY/PARKED/NOTIFIED）
     - `mutex`: 互斥锁用于协调线程阻塞
     - `condvar`: 条件变量用于线程等待和唤醒

2. **状态管理**
   - **状态常量**  
     `EMPTY`（空闲）、`PARKED`（已阻塞）、`NOTIFIED`（已唤醒）
   - **原子操作**  
     使用 `compare_exchange` 和 `swap` 确保线程安全的状态转换，避免竞态条件。

3. **阻塞与唤醒逻辑**
   - **park() 方法**  
     尝试快速路径（已通知则直接返回），否则通过 `condvar.wait()` 进入阻塞，循环处理虚假唤醒。
   - **park_timeout() 方法**  
     支持超时阻塞，针对 WebAssembly 等特殊平台提供兼容实现。
   - **unpark() 方法**  
     通过设置 `NOTIFIED` 状态并触发 `condvar.notify_one()` 唤醒线程，确保线程安全唤醒。

4. **辅助结构**
   - **CachedParkThread**  
     提供对当前线程 `ParkThread` 的访问，支持 `block_on()` 方法直接阻塞当前线程执行异步任务。
   - **RawWaker 集成**  
     通过 unsafe 代码实现与标准库 `Waker` 的兼容，将 `UnparkThread` 转换为任务调度所需的唤醒器。

---

#### 与项目的关系
该文件是 Tokio 运行时调度系统的底层基石，负责：
- 线程的高效阻塞与唤醒，减少 CPU 空转
- 协调异步任务的执行时机，确保事件驱动模型的正确性
- 提供与标准库 `Waker` 的集成，支持异步任务的协作调度
