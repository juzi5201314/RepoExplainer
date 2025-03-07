# `tokio/src/runtime/local_runtime/options.rs` 文件详解

## 文件目的
该文件定义了 Tokio Local Runtime 的专用配置选项结构体 `LocalOptions`。尽管当前未提供任何实际配置项，但通过类型系统设计确保了该结构体的类型安全特性，并为未来扩展预留了空间。

---

## 关键组件

### 1. `LocalOptions` 结构体
```rust
#[derive(Default, Debug)]
#[non_exhaustive]
pub struct LocalOptions {
    _phantom: PhantomData<*mut u8>,
}
```

#### 核心特性：
- **类型标记**：通过 `PhantomData<*mut u8>` 标记该结构体为 `!Send + !Sync`。由于 `*mut u8` 不实现 `Send` 和 `Sync`，此标记确保 `LocalOptions` 的实例无法跨线程共享或传递。
- **默认实现**：通过 `#[derive(Default)]` 提供默认构造方法，方便用户直接使用 `LocalOptions::default()` 初始化。
- **调试支持**：`#[derive(Debug)]` 允许通过 `println!("{:?}", options)` 输出调试信息。
- **非穷尽性**：`#[non_exhaustive]` 防止外部代码完全匹配该结构体，避免因未来字段扩展导致的编译错误。

#### 文档说明：
- 明确说明此结构体专用于 `LocalRuntime`，未来可能添加非 `Send` 和非 `Sync` 的钩子（如本地资源管理回调）。

---

### 2. `PhantomData` 的作用
- **类型安全**：通过持有 `PhantomData<*mut u8>`，结构体继承了原始类型的 `!Send + !Sync` 特性。这确保 `LocalOptions` 的使用者无法绕过线程限制。
- **内存零占用**：`PhantomData` 不实际占用内存空间，仅用于类型系统约束。

---

## 在项目中的角色
此文件是 Tokio Local Runtime 模块的配置基础设施。尽管当前无功能选项，但其设计为：
1. **类型安全边界**：通过 `!Send + !Sync` 防止配置对象被错误地跨线程使用。
2. **未来扩展准备**：预留接口用于添加本地运行时特有的配置（如非共享钩子）。
3. **模块化设计**：将配置逻辑与运行时核心分离，符合 Tokio 的模块化架构原则。

最后一行摘要：  