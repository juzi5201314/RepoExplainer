# 代码文件解释：`counters.rs`

## **目的**
该文件为Tokio多线程调度器提供可选的统计计数功能，用于跟踪调度器内部关键操作的执行次数。通过条件编译特性`tokio_internal_mt_counters`控制是否启用统计功能，便于调试和性能分析。

---

## **关键组件**

### **1. 统计计数器（启用时）**
当启用`tokio_internal_mt_counters`特性时，定义以下原子计数器：
- **`NUM_MAINTENANCE`**：维护任务执行次数（如清理过期任务）。
- **`NUM_NOTIFY_LOCAL`**：本地通知操作次数（如任务队列有新任务时通知本地线程）。
- **`NUM_UNPARKS_LOCAL`**：本地线程唤醒次数（如通过`park`/`unpark`机制唤醒线程）。
- **`NUM_LIFO_SCHEDULES`**：LIFO（后进先出）调度策略的使用次数。
- **`NUM_LIFO_CAPPED`**：因容量限制被截断的LIFO调度次数。

这些计数器使用`AtomicUsize`实现线程安全的无锁增量操作。

---

### **2. 统计计数器（禁用时）**
当禁用`tokio_internal_mt_counters`时，所有计数器相关函数被空实现，避免运行时开销：
```rust
pub(crate) fn inc_num_notify_local() {} // 空函数
pub(crate) fn inc_num_unparks_local() {} // 空函数
// 其他函数同理
```

---

### **3. `Counters`结构体**
- **`Drop`实现**：当`Counters`实例被销毁时（如程序结束），自动打印所有计数器的最终值，格式如下：
  ```
  ---
  notifies (local): 123
   unparks (local): 45
       maintenance: 6
    LIFO schedules: 78
       LIFO capped: 9
  ```
- **作用**：作为统计信息的汇总点，确保在程序退出前输出所有统计结果。

---

### **4. 计数器递增函数**
提供以下公共函数供调度器其他模块调用：
```rust
pub(crate) fn inc_num_notify_local() { ... }
pub(crate) fn inc_num_unparks_local() { ... }
pub(crate) fn inc_num_maintenance() { ... }
pub(crate) fn inc_lifo_schedules() { ... }
pub(crate) fn inc_lifo_capped() { ... }
```
这些函数通过原子操作安全地递增对应的计数器。

---

## **在项目中的角色**