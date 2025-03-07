# Tokio `Empty` I/O Utility

## Purpose
The `empty.rs` file provides an asynchronous implementation of a null I/O device. It implements `AsyncRead`, `AsyncBufRead`, `AsyncWrite`, and `AsyncSeek` traits to:
- Return EOF immediately on reads
- Discard all written data
- Report successful writes without storage
- Support no-op seeking

This serves as Tokio's equivalent of [`std::io::empty`](https://doc.rust-lang.org/std/io/fn.empty.html) for async operations.

## Key Components

### `Empty` Struct
- Zero-sized type with phantom field `_p` for marker purposes
- Implements core async I/O traits:
  - **AsyncRead**: Always returns 0 bytes (EOF)
  - **AsyncBufRead**: Provides empty buffers
  - **AsyncWrite**: Acknowledges writes without storage
  - **AsyncSeek**: Pretends to be a zero-length seekable object

### Core Functionality
1. **Reading** (`AsyncRead`):
   ```rust
   fn poll_read() -> Poll<io::Result<()>> {
       // Always reports successful read of 0 bytes
   }
   ```
2. **Writing** (`AsyncWrite`):
   ```rust
   fn poll_write() -> Poll<io::Result<usize>> {
       // Returns full buffer length as "written"
   }
   ```
3. **Buffered Reading** (`AsyncBufRead`):
   ```rust
   fn poll_fill_buf() -> Poll<io::Result<&[u8]>> {
       // Always returns empty slice
   }
   ```
4. **Seeking** (`AsyncSeek`):
   ```rust
   fn poll_complete() -> Poll<io::Result<u64>> {
       // Always reports position 0
   }
   ```

### Utility Features
- Cooperative yielding using `poll_proceed_and_make_progress`
- Vectorized write support through `poll_write_vectored`
- Unpin implementation for safe async usage
- Debug formatting that hides implementation details

## Integration with Tokio
This implementation:
- Works with Tokio's async task system through proper `Poll` handling
- Integrates with tracing infrastructure via `trace_leaf` calls
- Complements other I/O utilities in `tokio::io::util`
- Serves as a building block for testing and I/O redirection scenarios

## Example Use Cases
1. **Discarding Output**:
   ```rust
   let mut sink = tokio::io::empty();
   sink.write_all(b"discarded data").await?;
   ```
2. **Empty Input Sources**:
   ```rust
   let mut buffer = Vec::new();
   tokio::io::empty().read_to_end(&mut buffer).await?;
   // buffer remains empty
   ```

## Testing
Includes a basic test to verify `Unpin` implementation, ensuring compatibility with async move semantics.

---
