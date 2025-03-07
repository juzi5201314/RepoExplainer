## Tokio I/O Utility: `write_all_buf.rs`

### Purpose
This file implements an asynchronous future (`WriteAllBuf`) to write the entire contents of a buffer (`Buf`) to an `AsyncWrite` target. It handles both regular and vectored I/O operations efficiently, ensuring all data is written or an error is returned.

### Key Components
1. **Struct `WriteAllBuf`**:
   - A `Future` that persists mutable references to:
     - `writer`: The asynchronous writer (`AsyncWrite + Unpin`)
     - `buf`: The buffer (`Buf`) containing data to write
   - Uses `PhantomPinned` to enforce pinning semantics for safe async usage.

2. **Constructor `write_all_buf`**:
   - Creates a `WriteAllBuf` future, initializing it with the writer and buffer references.

3. **Future Implementation**:
   - **Poll Logic**:
     - Continuously writes buffer data until exhausted.
     - Uses vectored writes (`poll_write_vectored`) if supported by the writer (up to 64 slices).
     - Falls back to regular writes (`poll_write`) otherwise.
     - Advances the buffer cursor after each successful write.
     - Returns `WriteZero` error if no progress is made (n=0).
   - **Termination**:
     - Completes with `Ok(())` when the buffer is fully written.
     - Propagates I/O errors from the underlying writer.

### Integration with Project
- Part of Tokio's asynchronous I/O utilities, complementing other futures like `WriteAll` and `WriteBuf`.
- Works with the `AsyncWrite` trait hierarchy, enabling composable I/O operations.
- Leverages `bytes::Buf` for efficient buffer management, common in network protocols.
- Integrates with Tokio's runtime to enable non-blocking I/O operations.

### Related Context
- Similar to `WriteAll` (for byte slices) but designed for `Buf` types.
- Uses `poll_write_vectored` for scatter/gather I/O optimizations.
- Interacts with other I/O primitives like `BufWriter` and `CopyBuffer` in the Tokio ecosystem.

---
