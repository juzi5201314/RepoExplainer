# `either.rs` 文件详解

## 文件目的
该文件定义了一个泛型枚举类型 `Either`，用于将两种不同但具有相同关联类型的异步类型（如 Future、Stream、Sink 等）统一为单一类型。其核心作用是解决 Rust 编译器对分支返回不同异步类型时的类型不匹配问题。

## 关键组件

### 1. `Either` 枚举类型
```rust
pub enum Either<L, R> {
    Left(L),
    Right(R),
}
```
- **功能**：通过 `Left` 和 `Right` 变体，将两种不同类型的值包装为统一类型。
- **特性**：
  - 实现 `Debug` 和 `Clone` 衍生 trait。
  - 支持异步编程中的核心 trait（如 `Future`、`AsyncRead`、`Stream` 等）。

### 2. `delegate_call!` 宏
```rust
macro_rules! delegate_call {
    ($self:ident.$method:ident($($args:ident),+)) => {
        // 根据变体类型调用对应方法
    }
}
```
- **作用**：通过宏减少 trait 实现的重复代码，自动将方法调用分派到 `Either` 的具体变体。
- **原理**：使用 `unsafe` 代码处理 `Pin` 引用，确保对 `Left` 或 `Right` 的安全访问。

### 3. 异步 trait 实现
为 `Either` 实现了以下核心异步 trait：
- **`Future`**：通过 `poll` 方法将轮询操作分派到内部变体。
- **`AsyncRead/AsyncWrite/AsyncSeek`**：实现 Tokio 的异步 I/O trait，支持流式读写和定位操作。
- **`Stream`**：作为异步流，支持 `poll_next` 方法。
- **`Sink`**：实现 Futures 的 Sink trait，支持异步数据发送。

### 4. 示例与测试
- **示例**：展示了如何通过 `Either` 统一不同 Future 类型，解决编译错误。
- **测试**：
  - `either_is_stream`：验证 `Either` 作为流的正确性。
  - `either_is_async_read`：测试异步读取功能。

## 在项目中的角色
该文件为 Tokio 生态系统提供了统一的类型包装器，允许开发者在条件分支中安全地处理不同但功能兼容的异步类型（如不同 Future 或流），确保代码的类型一致性与可维护性。
