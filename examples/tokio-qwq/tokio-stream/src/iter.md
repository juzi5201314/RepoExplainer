# 文件说明：`tokio-stream/src/iter.rs`

## **目的**
该文件实现了将 Rust 标准库的 `Iterator` 转换为 Tokio 异步 `Stream` 的适配器。通过 `iter` 函数将同步迭代器包装为异步流，使其能在异步环境中使用。

---

## **核心组件**

### **1. `Iter` 结构体**
```rust
pub struct Iter<I> {
    iter: I,
    yield_amt: usize,
}
```
- **字段说明**：
  - `iter`: 存储原始迭代器（`Iterator` 类型）。
  - `yield_amt`: 计数器，用于控制 `poll_next` 的调用频率，防止过度轮询。

- **特性**：
  - `Unpin` 实现：确保该结构体可以安全地被移动。
  - `#[must_use]` 属性：强制用户必须使用流，否则会触发编译警告。

---

### **2. `iter` 函数**
```rust
pub fn iter<I>(i: I) -> Iter<I::IntoIter>
where
    I: IntoIterator,
{
    Iter {
        iter: i.into_iter(),
        yield_amt: 0,
    }
}
```
- **功能**：将任意 `IntoIterator` 类型转换为 `Iter` 实例。
- **作用**：提供统一接口将同步迭代器（如 `Vec`、`Range` 等）转换为异步流。

---

### **3. `Stream` Trait 实现**
```rust
impl<I> Stream for Iter<I>
where
    I: Iterator,
{
    // ...
}
```
#### **关键方法**
- **`poll_next` 方法**
```rust
fn poll_next(...) -> Poll<Option<I::Item>> {
    if self.yield_amt >= 32 {
        // 每 32 次轮询后暂停，唤醒调度器
        self.yield_amt = 0;
        cx.waker().wake_by_ref();
        Poll::Pending
    } else {
        self.yield_amt += 1;
        Poll::Ready(self.iter.next())
    }
}
```
- **行为**：
  - 每连续调用 32 次 `poll_next` 后，主动返回 `Pending`，让出执行权，避免阻塞事件循环。
  - 通过 `yield_amt` 控制轮询频率，平衡性能与调度公平性。
  - 注释提到 `TODO` 需要补充协作调度（coop）逻辑，可能后续版本会优化。

- **`size_hint` 方法**
```rust
fn size_hint(&self) -> (usize, Option<usize>) {
    self.iter.size_hint()
}
```
- **功能**：直接转发迭代器的大小估计，供流操作符（如 `take`）使用。

---

## **使用场景**
通过 `stream::iter` 可以将同步数据结构（如 `Vec`、`Range`）快速转换为异步流，支持以下操作：
```rust
let stream = stream::iter(vec![1, 2, 3]);
stream.next().await; // 异步获取元素
stream.peekable();   // 添加预读功能
stream.skip_while(...); // 组合流操作符
```

---

## **项目中的角色**