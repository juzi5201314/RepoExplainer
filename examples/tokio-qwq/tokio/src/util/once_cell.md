# `once_cell.rs` 文件解析

## 概述
该文件实现了 `OnceCell<T>` 结构体，这是一个线程安全的惰性初始化容器。它确保某个值在首次访问时被初始化，并且后续访问直接返回已初始化的值。该结构体是 Tokio 异步运行时内部使用的工具类，用于需要跨线程安全初始化的场景。

---

## 核心组件

### 1. **结构体定义**
```rust
pub(crate) struct OnceCell<T> {
    once: Once,
    value: UnsafeCell<MaybeUninit<T>>,
}
```
- **`once`**：使用标准库的 `std::sync::Once` 确保初始化逻辑仅执行一次。
- **`value`**：通过 `UnsafeCell` 包裹 `MaybeUninit<T>`，允许内部可变性，同时利用 `MaybeUninit` 安全地处理未初始化内存。

### 2. **安全标注**
```rust
unsafe impl<T: Send + Sync> Send for OnceCell<T> {}
unsafe impl<T: Send + Sync> Sync for OnceCell<T> {}
```
- 通过标注 `Send` 和 `Sync`，表明当 `T` 同时满足 `Send` 和 `Sync` 时，`OnceCell<T>` 可安全跨线程共享。

---

## 核心方法

### 3. **初始化方法**
```rust
pub(crate) const fn new() -> Self {
    Self {
        once: Once::new(),
        value: UnsafeCell::new(MaybeUninit::uninit()),
    }
}
```
- 使用 `const fn` 实现常量初始化，初始时 `value` 处于未初始化状态。

### 4. **值获取与初始化**
```rust
pub(crate) fn get(&self, init: impl FnOnce() -> T) -> &T {
    if !self.once.is_completed() {
        self.do_init(init);
    }
    unsafe { &*(self.value.get() as *const T) }
}
```
- **惰性初始化**：首次调用时触发初始化逻辑。
- **线程安全**：通过 `Once` 确保初始化仅执行一次，且后续访问直接返回已初始化值。
- **错误处理**：若 `init` 闭包 panic，`Once` 会标记为“中毒”，后续调用将直接 panic。

### 5. **初始化逻辑**
```rust
fn do_init(&self, init: impl FnOnce() -> T) {
    let value_ptr = self.value.get() as *mut T;
    self.once.call_once(|| {
        let set_to = init();
        unsafe { std::ptr::write(value_ptr, set_to); }
    });
}
```
- **原子操作**：通过 `call_once` 确保初始化闭包仅执行一次。
- **内存安全**：利用指针操作将初始化后的值写入未初始化内存，依赖 `Once` 的线程安全保证。

### 6. **析构方法**
```rust
impl<T> Drop for OnceCell<T> {
    fn drop(&mut self) {
        if self.once.is_completed() {
            unsafe { std::ptr::drop_in_place(self.value.get() as *mut T); }
        }
    }
}
```
- **手动析构**：若值已初始化，则调用其析构函数释放资源。

---

## 工作原理
1. **首次访问**：调用 `get` 时检查 `once` 是否完成，未完成则触发初始化。
2. **线程安全初始化**：通过 `Once` 确保初始化逻辑原子性，避免竞争条件。
3. **内存安全**：利用 `MaybeUninit` 和指针操作，确保未初始化内存不会被错误访问。
4. **高效访问**：初始化后直接返回已初始化值的引用，无需额外同步开销。

---

## 项目中的角色
该文件为 Tokio 提供了线程安全的惰性初始化机制，用于确保关键资源（如信号处理、内部状态）仅初始化一次且跨线程安全访问，是 Tokio 内部实现高效资源管理的核心工具之一。
