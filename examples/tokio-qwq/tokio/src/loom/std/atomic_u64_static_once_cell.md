### 文件说明：StaticAtomicU64 实现

#### 文件目的
该文件为 Tokio 项目中的 loom 测试框架提供了一个基于 `Mutex` 的原子操作实现，用于在静态变量场景下安全地操作 64 位无符号整数。通过结合 `OnceCell` 和 `Mutex`，确保线程安全的初始化和原子操作。

#### 关键组件
1. **结构体定义**
   ```rust
   pub(crate) struct StaticAtomicU64 {
       init: u64,
       cell: OnceCell<Mutex<u64>>,
   }
   ```
   - `init`: 初始值，用于延迟初始化时创建 `Mutex`
   - `cell`: 延迟初始化容器，内部存储 `Mutex<u64>` 实例

2. **初始化方法**
   ```rust
   pub(crate) const fn new(val: u64) -> StaticAtomicU64 {
       StaticAtomicU64 { init: val, cell: OnceCell::new() }
   }
   ```
   使用 `const fn` 实现常量初始化，确保静态变量的编译期初始化能力。

3. **核心操作方法**
   - **加载值**
     ```rust
     pub(crate) fn load(&self, _order: Ordering) -> u64 {
         *self.inner().lock()
     }
     ```
     通过 `Mutex` 锁获取当前值，参数 `_order` 保留原子操作接口但实际未使用。

   - **原子加法**
     ```rust
     pub(crate) fn fetch_add(&self, val: u64, _order: Ordering) -> u64 {
         let mut lock = self.inner().lock();
         let prev = *lock;
         *lock = prev + val;
         prev
     }
     ```
     在锁保护下执行加法操作，返回旧值。

   - **比较并交换**
     ```rust
     pub(crate) fn compare_exchange_weak(...) -> Result<u64, u64> {
         let mut lock = self.inner().lock();
         if *lock == current { ... }
     }
     ```
     在锁保护下实现 CAS 操作，确保线程安全。

4. **内部初始化逻辑**
   ```rust
   fn inner(&self) -> &Mutex<u64> {
       self.cell.get(|| Mutex::new(self.init))
   }
   ```
   使用 `OnceCell` 延迟初始化 `Mutex`，确保首次访问时线程安全地创建实例。

#### 项目中的作用
该文件为 Tokio 的 loom 测试框架提供了兼容原子操作的静态变量实现，通过 `Mutex` 和 `OnceCell` 的组合，在模拟多线程环境中保证线程安全的原子操作能力。特别适用于需要静态初始化且要求原子性的场景（如计数器、状态标志），为 Tokio 的并发测试和运行时提供了底层支持。

#### 在项目中的角色