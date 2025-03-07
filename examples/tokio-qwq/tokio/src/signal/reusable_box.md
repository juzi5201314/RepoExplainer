### 文件说明：ReusableBoxFuture 结构体详解

#### 文件目的
该文件实现了 `ReusableBoxFuture<T>` 结构体，用于在不频繁重新分配内存的情况下，安全地复用 `Pin<Box<dyn Future<Output = T> + Send>>` 的内存空间。通过比较新旧 Future 的内存布局（大小和对齐方式），在布局一致时直接复用现有内存，从而减少内存分配开销，提升异步任务的执行效率。

---

#### 核心组件与功能

1. **结构体定义**
   ```rust
   pub(crate) struct ReusableBoxFuture<T> {
       boxed: NonNull<dyn Future<Output = T> + Send>,
   }
   ```
   - 使用 `NonNull` 指针管理动态调度的 Future 对象，确保指针始终有效。
   - 内部存储的是 `dyn Future<Output = T> + Send` 的非空原始指针。

2. **创建与初始化**
   ```rust
   pub(crate) fn new<F>(future: F) -> Self
   ```
   - 将传入的 Future 转换为 `Box<dyn Future>`，通过 `Box::into_raw` 转换为原始指针，并封装为 `NonNull`。

3. **Future 替换机制**
   - **`set` 方法**：尝试直接复用现有内存，若布局不匹配则强制重新分配。
     ```rust
     pub(crate) fn set<F>(&mut self, future: F) { ... }
     ```
   - **`try_set` 方法**：仅在布局匹配时替换 Future，否则返回错误。
     ```rust
     pub(crate) fn try_set<F>(&mut self, future: F) -> Result<(), F> { ... }
     ```
   - **`set_same_layout` 安全操作**：在布局一致时，直接覆盖内存并更新虚函数表：
     ```rust
     unsafe fn set_same_layout<F>(&mut self, future: F) { ... }
     ```
     - 安全释放旧 Future（捕获 panic）
     - 直接写入新 Future 到相同内存地址
     - 更新虚指针以保持动态分派能力

4. **Future 接口实现**
   ```rust
   impl<T> Future for ReusableBoxFuture<T> {
       fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<T> { ... }
   }
   ```
   - 通过 `get_pin` 方法获取内部 Future 的 `Pin` 引用，确保安全的移动语义。
   - `poll` 方法直接委托给内部 Future 的 `poll` 实现。

5. **内存管理**
   - **Drop 实现**：通过 `Box::from_raw` 确保内存正确释放。
   - **Sync/Send 安全性**：通过 unsafe impl 标记为 `Send` 和 `Sync`，满足异步运行时的跨线程需求。

---

#### 关键特性
- **内存复用优化**：通过比较 `Layout` 避免不必要的内存分配，适用于频繁替换 Future 的场景（如信号处理）。
- **panic 安全**：在替换 Future 时捕获旧 Future 的析构 panic，确保内存状态一致性。
- **零成本抽象**：通过 raw pointer 和 unsafe 操作实现高效内存管理，同时保持类型安全。

---

#### 在项目中的角色
此文件为 Tokio 的信号处理模块提供了高效的 Future 管理机制。在信号事件循环中，可能需要频繁创建和替换 Future 对象（如等待信号的异步任务）。通过复用内存分配，显著减少了内存分配/释放的开销，从而提升信号处理的性能和吞吐量。
