# AtomicCell 结构体详解

## 概述
AtomicCell 是 Tokio 库中用于线程安全地管理可选值（Option<Box<T>>）的原子容器。它通过原子指针操作实现线程安全的值替换和获取功能，适用于需要共享可变状态的并发场景。

## 核心组件
### 1. 数据结构
```rust
pub(crate) struct AtomicCell<T> {
    data: AtomicPtr<T>,
}
```
- **AtomicPtr<T> 内核**：使用 loom 库的原子指针类型 AtomicPtr 来存储指向 Box<T> 的原始指针
- **安全标注**：通过 unsafe impl 显式标注 Send/Sync，表明该结构在满足 T: Send 条件下可安全跨线程使用

### 2. 核心方法
#### 初始化
```rust
pub(crate) fn new(data: Option<Box<T>>) -> AtomicCell<T> {
    AtomicCell { data: AtomicPtr::new(to_raw(data)), }
}
```
- 将输入的 Option<Box<T>> 转换为原始指针：
  - `to_raw` 函数将 Box 转为裸指针，None 时返回 NULL

#### 原子操作
```rust
pub(crate) fn swap(&self, val: Option<Box<T>>) -> Option<Box<T>> {
    let old = self.data.swap(to_raw(val), AcqRel);
    from_raw(old)
}
```
- 使用原子交换操作（AcqRel 顺序）实现线程安全的值替换：
  - 返回旧值并保持内存同步
  - 支持 None 参数实现"取走"操作

#### 辅助方法
```rust
pub(crate) fn set(&self, val: Box<T>) { self.swap(Some(val)); }
pub(crate) fn take(&self) -> Option<Box<T>> { self.swap(None) }
```
- `set`：设置新值并丢弃旧值
- `take`：原子取出当前值（设置为 None）

### 3. 内存管理
```rust
impl<T> Drop for AtomicCell<T> {
    fn drop(&mut self) { let _ = self.take(); }
}
```
- 在结构体销毁时自动清理未被取出的值，防止内存泄漏

## 实现细节
### 原始指针转换
```rust
fn to_raw<T>(data: Option<Box<T>>) -> *mut T {
    data.map_or(ptr::null_mut(), Box::into_raw)
}

fn from_raw<T>(val: *mut T) -> Option<Box<T>> {
    if val.is_null() { None } else { unsafe { Some(Box::from_raw(val)) } }
}
```
- 将 Box 转换为裸指针（to_raw）
- 通过 unsafe 从裸指针恢复 Box（from_raw）

## 在 Tokio 项目中的角色
AtomicCell 是 Tokio 内部实现线程安全状态管理的基础组件，提供：
1. 原子化的值替换操作（swap）
2. 安全的跨线程数据共享
3. 自动内存管理保障
常用于需要原子操作的场景，如资源管理、状态机切换等需要线程安全共享可变状态的场景。
