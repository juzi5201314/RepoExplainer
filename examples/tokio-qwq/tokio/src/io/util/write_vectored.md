# 文件说明：`tokio/src/io/util/write_vectored.rs`

## **功能与目的**  
该文件定义了一个异步 future `WriteVectored`，用于将一组缓冲区（`IoSlice` 切片）异步写入实现了 `AsyncWrite` 的 I/O 对象。其核心目标是提供高效的非阻塞写操作，支持向底层 I/O 资源批量写入多个缓冲区，减少系统调用次数，提升性能。

---

## **关键组件与实现细节**

### **1. `WriteVectored` 结构体**
```rust
pin_project! {
    pub struct WriteVectored<'a, 'b, W: ?Sized> {
        writer: &'a mut W,
        bufs: &'a [IoSlice<'b>],
        _pin: PhantomPinned,
    }
}
```
- **字段说明**：
  - `writer`: 需要写入的异步写对象（实现了 `AsyncWrite`）。
  - `bufs`: 待写入的缓冲区切片（`IoSlice` 类型，代表不可变字节切片）。
  - `_pin`: 通过 `PhantomPinned` 确保该 future 是 `!Unpin` 的，以兼容异步 trait 方法的要求。
- **特性**：
  - 使用 `pin_project` 宏管理内部可变性和 pin 语义，确保结构体在堆上分配时能正确处理移动操作。
  - `#[must_use]` 属性强制用户必须 `await` 或显式轮询该 future，避免未使用的异步操作。

---

### **2. 构造函数 `write_vectored`**
```rust
pub(crate) fn write_vectored<'a, 'b, W>(
    writer: &'a mut W,
    bufs: &'a [IoSlice<'b>],
) -> WriteVectored<'a, 'b, W>
where
    W: AsyncWrite + Unpin + ?Sized,
{
    WriteVectored { writer, bufs, _pin: PhantomPinned }
}
```
- **作用**：创建 `WriteVectored` 实例，参数包括目标写对象和缓冲区切片。
- **约束**：要求 `W` 实现 `AsyncWrite` 且为 `Unpin`，确保 future 可以安全地被存储和移动。

---

### **3. Future 实现**
```rust
impl<W> Future for WriteVectored<'_, '_, W>
where
    W: AsyncWrite + Unpin + ?Sized,
{
    type Output = io::Result<usize>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<usize>> {
        let me = self.project();
        Pin::new(&mut *me.writer).poll_write_vectored(cx, me.bufs)
    }
}
```
- **核心逻辑**：
  - 在 `poll` 方法中，通过 `project` 解构结构体字段。
  - 调用 `writer` 的 `poll_write_vectored` 方法执行实际的异步写操作。
  - 返回写入的字节数或错误，遵循 `AsyncWrite` 的标准行为。

---

## **项目中的角色**
该文件是 Tokio 异步 I/O 框架的一部分，提供高效的 **向量写操作（Vectored Write）** 支持。通过将多个缓冲区合并为单次异步写请求，减少系统调用开销，优化网络或文件 I/O 性能。它与 `AsyncWrite` 接口深度集成，是 Tokio 处理批量数据写入的核心工具。
