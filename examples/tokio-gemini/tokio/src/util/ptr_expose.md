这个文件 `ptr_expose.rs` 的主要目的是帮助 Miri（一个 Rust 代码的内存模型检查器）理解 Tokio 框架中暴露的指针。在正常执行时，这个模块等同于指针转换。然而，当在 Miri 下运行时，指针转换会被替换为哈希映射查找。这使得 Tokio 在 Miri 下运行时能够兼容严格的来源追踪（strict provenance），尽管这会带来性能开销。

**关键组件：**

*   `PtrExposeDomain<T>` 结构体：
    *   `#[cfg(miri)] map: Mutex<BTreeMap<usize, *const T>>`：在 Miri 下，这是一个互斥锁保护的 `BTreeMap`，用于存储指针的地址和原始指针。
    *   `_phantom: PhantomData<T>`：一个零大小的标记，用于确保 `PtrExposeDomain` 拥有类型 `T` 的所有权，即使它不直接存储 `T` 的值。
*   `unsafe impl<T> Sync for PtrExposeDomain<T> {}`：声明 `PtrExposeDomain` 是 `Sync` 的，因为实际上使用指针是不安全的，所以跨线程传递它们是安全的。
*   `new()` 方法：创建一个新的 `PtrExposeDomain` 实例。在 Miri 下，它会初始化一个空的 `BTreeMap`。
*   `expose_provenance(&self, ptr: *const T) -> usize` 方法：
    *   在 Miri 下，它将指针转换为其地址（`usize`），并将地址和原始指针存储在哈希映射中。
    *   在非 Miri 下，它简单地将指针转换为其地址。
    *   这个方法“暴露”了指针的来源，以便 Miri 能够跟踪它。
*   `from_exposed_addr(&self, addr: usize) -> *const T` 方法：
    *   在 Miri 下，它从哈希映射中查找与给定地址关联的原始指针。如果找不到，会触发 Miri 错误。
    *   在非 Miri 下，它将地址转换为指针。
    *   这个方法从暴露的地址中“恢复”指针。
*   `unexpose_provenance(&self, _ptr: *const T)` 方法：
    *   在 Miri 下，它从哈希映射中移除与给定指针地址关联的条目。如果找不到，会触发 Miri 错误。
    *   这个方法“取消暴露”指针的来源。

**与项目的关系：**

这个文件是 Tokio 框架的一部分，用于在 Miri 下运行时提供对指针来源的正确跟踪。它通过在 Miri 下使用哈希映射来模拟指针转换，从而确保 Tokio 代码在 Miri 的严格内存模型下能够正确运行。这有助于发现潜在的内存安全问题。
