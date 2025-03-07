# 文件解释：`tokio/src/io/util/write_all.rs`

## **目的**
该文件实现了异步写入所有数据的 Future `WriteAll`，确保在异步环境中将指定字节缓冲区（`&[u8]`）完整写入到实现了 `AsyncWrite` trait 的目标流中。

---

## **关键组件**

### **1. `WriteAll` 结构体**
```rust
pin_project! {
    #[derive(Debug)]
    pub struct WriteAll<'a, W: ?Sized> {
        writer: &'a mut W,
        buf: &'a [u8],
        _pin: PhantomPinned,
    }
}
```
- **字段说明**：
  - `writer`: 目标异步写入流的可变引用，需实现 `AsyncWrite`。
  - `buf`: 待写入的字节缓冲区。
  - `_pin`: 使用 `PhantomPinned` 标记结构体为 `!Unpin`，确保 Future 在异步操作中被正确 `Pin`。

### **2. `write_all` 工厂函数**
```rust
pub(crate) fn write_all<'a, W>(writer: &'a mut W, buf: &'a [u8]) -> WriteAll<'a, W> { ... }
```
- **功能**：创建 `WriteAll` Future 的实例，初始化写入目标和缓冲区。

### **3. `Future` 实现**
```rust
impl<W> Future for WriteAll<'_, W> where W: AsyncWrite + Unpin + ?Sized {
    type Output = io::Result<()>;

    fn poll(...) { ... }
}
```
- **核心逻辑**：
  1. 循环调用 `poll_write` 将 `buf` 分段写入流。
  2. 根据每次写入的字节数 `n` 更新剩余缓冲区。
  3. 若 `n == 0`（无效写入），返回错误；否则继续直到 `buf` 为空。
  4. 成功时返回 `Poll::Ready(Ok(()))`。

---

## **技术细节**
- **Pin 安全性**：通过 `PhantomPinned` 和 `pin_project` 宏确保结构体在堆上分配后地址不被移动，符合异步 Future 的语义。
- **错误处理**：检测写入零字节的情况（如写入无效句柄），返回 `WriteZero` 错误。
- **零拷贝优化**：直接操作引用而非所有权，避免不必要的内存拷贝。

---

## **项目中的角色**
该文件为 Tokio 提供了异步写入所有数据的原子性操作，确保在异步流中可靠地完成完整写入，是 Tokio 异步 IO 工具库的核心组件之一。
