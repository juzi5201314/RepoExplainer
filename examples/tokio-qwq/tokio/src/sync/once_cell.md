### 文件说明：`tokio/src/sync/once_cell.rs`

#### **文件目的**
该文件实现了 `OnceCell<T>` 结构体，这是一个线程安全的单元（cell），允许仅初始化一次的值。它支持异步初始化，适用于需要在首次使用时初始化的全局变量或共享资源。

---

#### **核心组件与功能**

1. **结构体定义**
   ```rust
   pub struct OnceCell<T> {
       value_set: AtomicBool,      // 原子标志，标记值是否已设置
       value: UnsafeCell<MaybeUninit<T>>, // 存储实际值的未初始化内存
       semaphore: Semaphore,       // 信号量，控制初始化过程的独占访问
   }
   ```
   - **`value_set`**：原子布尔值，标记值是否已初始化。
   - **`value`**：使用 `UnsafeCell` 包装的未初始化内存，用于存储实际值。
   - **`semaphore`**：信号量用于确保仅一个线程执行初始化操作，其他线程等待。

2. **关键方法**
   - **`get_or_init` 和 `get_or_try_init`**：
     - 异步方法，尝试获取值。若未初始化，则执行异步闭包初始化值。
     - 使用信号量确保仅一个线程执行初始化，其他线程等待。
     - 示例：
       ```rust
       async fn get_global_integer() -> &'static u32 {
           ONCE.get_or_init(|| async { 1 + 1 }).await
       }
       ```
   - **`set`**：
     - 同步设置值，若已初始化则返回错误。
     - 使用信号量检查是否有其他线程正在初始化。
   - **`initialized`**：
     - 检查值是否已设置。

3. **安全机制**
   - **原子操作**：`value_set` 使用原子操作保证线程安全。
   - **信号量控制**：初始化时独占信号量，确保唯一写入者。
   - **内存屏障**：通过 `Acquire` 和 `Release` 内存序保证可见性。

4. **错误处理**
   - **`SetError` 枚举**：
     - `AlreadyInitializedError`：值已存在。
     - `InitializingError`：其他线程正在初始化。

---

#### **实现细节**
- **初始化流程**：
  1. 调用 `get_or_init` 时，首先检查 `value_set`。
  2. 若未初始化，尝试获取信号量的许可（`permit`）。
  3. 持有许可的线程执行初始化，设置值并关闭信号量。
  4. 其他线程等待信号量释放，最终读取已初始化的值。
- **内存管理**：
  - 使用 `MaybeUninit` 安全地存储未初始化的值。
  - `Drop` 实现确保值在 `OnceCell` 销毁时被正确释放。

---

#### **项目中的角色**