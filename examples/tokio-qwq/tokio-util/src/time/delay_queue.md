### 文件说明：`tokio-util/src/time/delay_queue.rs`

#### **目的**  
`DelayQueue` 是一个基于时间轮（Timer Wheel）实现的延迟队列，用于在指定时间后返回元素。它允许用户插入带有截止时间的元素，并在截止时间到达时通过流（Stream）接口获取这些元素。该队列适用于需要定时处理任务的场景，例如缓存过期、任务调度等。

---

#### **核心组件与功能**

1. **结构定义**  
   ```rust
   pub struct DelayQueue<T> {
       slab: SlabStorage<T>,          // 存储元素的 slab，支持高效内存复用
       wheel: Wheel<Stack<T>>,        // 时间轮，用于跟踪元素的截止时间
       expired: Stack<T>,             // 已过期元素的栈
       delay: Option<Pin<Box<Sleep>>>,// 下一个唤醒时间的定时器
       // 其他状态变量...
   }
   ```
   - **SlabStorage**: 使用 `slab` 库管理内存，通过 `Key` 访问元素。支持 `compact` 方法回收空闲内存。
   - **时间轮（Wheel）**: 将元素按截止时间分桶存储，高效查询最早到期的元素。
   - **expired 栈**: 存储已过期但尚未被取出的元素，确保优先处理。

2. **关键方法**  
   - **插入元素**  
     ```rust
     pub fn insert_at(&mut self, value: T, when: Instant) -> Key {
         // 计算截止时间，插入 slab，并更新时间轮或 expired 栈
     }
     ```
     - 元素插入后，通过 `Key` 可以修改或删除。
   - **获取过期元素**  
     ```rust
     pub fn poll_expired(&mut self, cx: &mut Context<'_>) -> Poll<Option<Expired<T>>> {
         // 检查 expired 栈或时间轮，返回最早到期的元素
     }
     ```
     - 实现 `Stream` trait，通过 `poll_expired` 拉取过期元素。
   - **修改截止时间**  
     ```rust
     pub fn reset_at(&mut self, key: &Key, when: Instant) {
         // 从原位置移除元素，重新插入新截止时间
     }
     ```

3. **时间轮机制**  
   - 时间轮将时间划分为多个层级的桶（如毫秒、秒、分钟），元素按截止时间插入对应的桶。
   - 当前时间通过 `wheel_now` 跟踪，定期轮询时间轮以查找最早到期的元素。
   - `delay` 定时器用于在下一个截止时间前唤醒任务，避免频繁轮询。

4. **内存管理**  
   - **SlabStorage 的 `Key` 映射**:  
     - `Key` 是用户可见的标识符，内部通过 `key_map` 处理 `compact` 后的索引变化。
     - `compact` 方法重组 slab，回收碎片，但需更新 `key_map` 以维护映射关系。
   - **过期元素优先处理**:  
     已过期的元素直接存入 `expired` 栈，确保 `poll_expired` 优先返回这些元素。

---

#### **实现细节**  
- **精度与粒度**: 截止时间以毫秒为单位，确保与 Tokio 定时器兼容。
- **高效查询**: 时间轮的层级结构（如 `wheel`）允许 O(1) 时间获取最早到期元素。
- **任务唤醒**: `delay` 定时器在下一个截止时间前唤醒任务，避免不必要的轮询。

---

#### **使用场景示例**  
```rust
// 缓存过期管理示例
struct Cache<K, V> {
    entries: HashMap<K, (V, Key)>,
    expirations: DelayQueue<K>,
}

impl<K, V> Cache<K, V> {
    fn insert(&mut self, key: K, value: V) {
        let delay = self.expirations.insert(key.clone(), Duration::from_secs(30));
        self.entries.insert(key, (value, delay));
    }

    fn poll_purge(&mut self, cx: &mut Context<'_>) -> Poll<()> {
        while let Some(expired_key) = ready!(self.expirations.poll_expired(cx)) {
            self.entries.remove(expired_key.get_ref());
        }
        Poll::Ready(())
    }
}
```

---

#### **在项目中的角色**  