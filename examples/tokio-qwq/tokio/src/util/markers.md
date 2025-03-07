# 文件说明：`tokio/src/util/markers.rs`

## **目的**  
该文件定义了用于标记特定线程安全特性的零大小类型（ZST），帮助 Tokio 在异步运行时中精确控制 `Send` 和 `Sync` 自动特质的实现。这些标记类型通过显式实现或拒绝实现 `Send`/`Sync` 特质，确保类型在并发场景中的安全性和预期行为。

---

## **关键组件**

### **1. `SyncNotSend` 结构体**
```rust
pub(crate) struct SyncNotSend(#[allow(dead_code)] *mut ());
unsafe impl Sync for SyncNotSend {}
```
- **作用**：标记一个类型为 `Sync`（可安全共享不可变引用）但 **非 `Send`**（不可跨线程传递）。
- **实现细节**：
  - 使用 `*mut ()` 原始指针作为字段（但被 `#[allow(dead_code)]` 忽略未使用警告），确保其零大小特性。
  - 通过 `unsafe impl Sync` 显式实现 `Sync` 特质，但未实现 `Send`，因此该类型默认为 `!Send`。
- **用途**：当某个类型需要被多个线程安全访问（`Sync`），但禁止跨线程传递（`!Send`）时，可通过包含 `SyncNotSend` 字段来继承其特性。

### **2. `NotSendOrSync` 结构体**
```rust
cfg_rt! {
    pub(crate) struct NotSendOrSync(#[allow(dead_code)] *mut ());
}
```
- **作用**：标记一个类型既 **非 `Send`** 也 **非 `Sync`**。
- **实现细节**：
  - 通过 `cfg_rt!` 宏配置，仅在 Tokio 运行时相关配置下生效。
  - 同样使用零大小的 `*mut ()` 字段，且未显式实现任何自动特质，因此默认为 `!Send + !Sync`。
- **用途**：用于需要严格限制线程安全性的场景，例如某些内部状态管理。

---

## **技术细节**
1. **零大小类型（ZST）**  
   两个结构体均通过 `*mut ()` 字段实现零大小特性，确保它们不会占用实际内存空间，仅作为标记存在。

2. **自动特质的显式控制**  
   - `unsafe impl Sync for SyncNotSend` 显式为 `SyncNotSend` 实现 `Sync` 特质，但未实现 `Send`，因此其类型默认为 `!Send`。
   - `NotSendOrSync` 未实现任何自动特质，因此其类型默认既非 `Send` 也非 `Sync`。

3. **配置宏 `cfg_rt!`**  
   `NotSendOrSync` 的定义被包裹在 `cfg_rt!` 宏中，表明其仅在 Tokio 运行时相关配置下生效，可能与不同运行时模式或编译时特性相关。

---

## **与项目的关系**
该文件是 Tokio 内部工具模块的一部分，通过提供精确控制 `Send` 和 `Sync` 特质的标记类型，确保运行时组件（如通道、任务等）在并发场景中的线程安全性。这些标记类型帮助 Tokio 在复杂异步操作中避免数据竞争，同时遵守 Rust 的所有权和并发模型。

---
