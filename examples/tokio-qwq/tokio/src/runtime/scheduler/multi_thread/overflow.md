# 文件说明：溢出处理机制实现

## 文件目的
该文件定义了Tokio多线程运行时调度器中的溢出处理机制，用于在任务队列满时将任务转移到其他线程或队列。通过抽象的`Overflow` trait提供统一的溢出接口，并为测试场景提供具体实现。

## 关键组件

### 1. `Overflow` trait
```rust
pub(crate) trait Overflow<T: 'static> {
    fn push(&self, task: task::Notified<T>);
    fn push_batch<I>(&self, iter: I) where I: Iterator<Item = task::Notified<T>>;
}
```
- **功能**：定义任务溢出的基本接口
- **方法**：
  - `push()`：单个任务溢出处理
  - `push_batch()`：批量任务溢出处理
- **约束**：`T: 'static`确保任务类型生命周期足够长，可安全跨线程调度

### 2. 测试实现
```rust
#[cfg(test)]
impl<T: 'static> Overflow<T> for RefCell<Vec<task::Notified<T>>> {
    fn push(&self, task: task::Notified<T>) {
        self.borrow_mut().push(task);
    }

    fn push_batch<I>(&self, iter: I) {
        self.borrow_mut().extend(iter);
    }
}
```
- **实现细节**：
  - 使用`RefCell<Vec<_>>`在测试中提供可变性
  - 通过`borrow_mut()`保证线程安全的可变访问
  - 将任务追加到向量末尾实现简单溢出模拟

## 工作原理
1. **溢出场景触发**：
   - 当任务队列（如单线程队列）无法容纳新任务时
   - 通过`push_back_or_overflow`方法调用溢出处理

2. **溢出处理流程**：
   - 调用`overflow.push()`或`overflow.push_batch()`
   - 将任务转移到实现`Overflow`的结构（测试中为向量）
   - 正式实现可能将任务转移到其他线程队列或调度器

## 项目角色