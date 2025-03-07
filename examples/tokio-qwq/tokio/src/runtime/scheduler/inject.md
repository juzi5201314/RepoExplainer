# Inject 队列实现文件说明

## 文件目的
该文件实现了 Tokio 运行时中用于向工作窃取调度器注入任务的 `Inject` 队列。该队列主要用于：
1. 将新任务注入调度器
2. 作为本地固定大小队列溢出时的后备队列
3. 处理任务唤醒事件

## 核心组件
### 1. 数据结构
```rust
pub(crate) struct Inject<T: 'static> {
    shared: Shared<T>,
    synced: Mutex<Synced>,
}
```
- **Shared<T>**：共享状态结构体，包含队列的核心数据（如任务存储、原子计数器等）
- **Mutex<Synced>**：通过互斥锁保护的同步状态，包含需要独占访问的同步原语（如条件变量等）

### 2. 关键模块
- **shared.rs**：定义 `Shared` 结构体，管理队列的共享状态
- **synced.rs**：定义需要线程安全保护的同步状态
- **pop.rs**：提供 `Pop` 类型，用于安全地弹出任务
- **metrics.rs**：（可选）性能指标统计模块

## 核心方法
### 初始化
```rust
pub(crate) fn new() -> Inject<T> {
    let (shared, synced) = Shared::new();
    Inject { shared, synced: Mutex::new(synced) }
}
```
通过 `Shared::new()` 初始化共享状态和同步状态。

### 关闭队列
```rust
pub(crate) fn close(&self) -> bool {
    let mut synced = self.synced.lock();
    self.shared.close(&mut synced)
}
```
将队列标记为关闭状态，返回是否成功关闭。

### 任务注入
```rust
pub(crate) fn push(&self, task: task::Notified<T>) {
    let mut synced = self.synced.lock();
    unsafe { self.shared.push(&mut synced, task) }
}
```
安全地将任务推入队列，若队列已关闭则忽略。

### 任务弹出
```rust
pub(crate) fn pop(&self) -> Option<task::Notified<T>> {
    let mut synced = self.synced.lock();
    unsafe { self.shared.pop(&mut synced) }
}
```
从队列中弹出任务，需要同步访问共享状态。

## 并发模型
- **MPMC 支持**：作为多生产者多消费者队列，允许：
  - 多个任务同时推送（生产者）
  - 多个工作者线程窃取或弹出任务（消费者）
- **原子操作**：通过 `loom` 库实现线程安全的原子操作
- **条件变量**：在 `Synced` 中可能包含等待队列非空的条件变量

## 项目中的角色
该文件是 Tokio 调度器的核心组件，负责：
1. 任务注入与唤醒事件的缓冲
2. 处理本地队列溢出时的任务转移
3. 支持多线程运行时的工作窃取机制
4. 提供线程安全的任务分发基础设施
