# Tokio Async Read Utility

## Purpose
This file implements an asynchronous read utility for Tokio's I/O operations. It provides a `Future`-based interface to read bytes into a buffer without blocking, enabling non-blocking I/O operations that integrate with Tokio's async runtime.

## Key Components

### `read` Function
- **Signature**: `pub(crate) fn read<'a, R>(reader: &'a mut R, buf: &'a mut [u8]) -> Read<'a, R>`
- Creates a `Read` future that asynchronously reads data into `buf` from the provided `reader`.
- Constraints: `R` must implement `AsyncRead + Unpin`.

### `Read` Future
- Defined via `pin_project!` macro to handle pinning safely.
- Contains:
  - Mutable references to the reader (`&'a mut R`) and buffer (`&'a mut [u8]`).
  - `PhantomPinned` to enforce !`Unpin` semantics, ensuring safe use in async contexts.

### Future Implementation
- `impl Future for Read<'_ R>`:
  - **Output**: `io::Result<usize>` indicating bytes read or errors.
  - **Polling Logic**:
    1. Wraps the buffer in a `ReadBuf` (Tokio's helper for tracking read progress).
    2. Polls the underlying reader via `poll_read`.
    3. Returns the number of bytes read using `buf.filled().len()`.

## Integration with Tokio
- Part of Tokio's I/O utilities, complementing other async I/O primitives like `AsyncWrite` and `AsyncBufRead`.
- Works with `AsyncRead` types (e.g., TCP streams, files) to enable non-blocking reads.
- Used internally by higher-level abstractions like `AsyncReadExt::read`.

## Related Context
- Interacts with `ReadBuf` for buffer management and `futures_io` compatibility layers.
- Shares patterns with other async I/O futures (e.g., `Seek`, `read_buf`) in Tokio's codebase.

---
