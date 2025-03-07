# 文件说明：`tokio/src/util/rand/rt.rs`

## **文件目的**
该文件实现了 Tokio 运行时中用于生成确定性随机种子的线程安全工具。通过封装 `FastRand` 随机数生成器，确保在多线程环境下生成的随机种子序列可复现，适用于需要可预测随机性的场景（如测试环境）。

---

## **核心组件**

### **1. `RngSeedGenerator` 结构体**
```rust
pub(crate) struct RngSeedGenerator {
    state: Mutex<FastRand>,
}
```
- **作用**：线程安全的随机种子生成器，基于 `Mutex` 包装 `FastRand` 实现跨线程安全访问。
- **关键特性**：
  - **确定性**：相同初始种子会生成完全相同的种子序列。
  - **线程安全**：通过 `Mutex` 锁保护内部状态，允许在多线程运行时安全使用。
  - **低开销设计**：注释提到种子生成频率较低，因此 `Mutex` 的锁竞争开销可忽略。

#### **方法**
- **`new(seed: RngSeed) -> Self`**  
  初始化生成器，使用给定种子创建 `FastRand` 实例并存入 `Mutex`。
- **`next_seed() -> RngSeed`**  
  生成下一个随机种子：
  ```rust
  let s = rng.fastrand();
  let r = rng.fastrand();
  RngSeed::from_pair(s, r)
  ```
  调用两次 `fastrand()` 方法生成种子的两个组成部分。
- **`next_generator() -> Self`**  
  使用 `next_seed()` 生成的新种子创建新的 `RngSeedGenerator` 实例，用于链式生成新生成器。

---

### **2. `FastRand` 结构体扩展**
```rust
impl FastRand {
    pub(crate) fn replace_seed(&mut self, seed: RngSeed) -> RngSeed { ... }
}
```
- **`replace_seed` 方法**  
  替换 `FastRand` 的内部状态为新种子，并返回旧状态：
  ```rust
  let old_seed = RngSeed::from_pair(self.one, self.two);
  self.one = seed.s;
  self.two = seed.r;
  old_seed
  ```
  用于保存和恢复随机数生成器的状态，确保可复现性。

---

## **与其他组件的关联**
- **运行时集成**：  
  通过 `runtime::Builder::new_current_thread().rng_seed(seed)` 设置初始种子，将 `RngSeedGenerator` 存入运行时句柄，供任务调度时使用。
- **线程局部存储对比**：  
  与直接使用线程局部的 `FastRand` 不同，该生成器需跨线程共享，因此需要 `Mutex` 保护。

---

## **项目中的角色**