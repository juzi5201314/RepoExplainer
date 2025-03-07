# Code File Explanation: `read_exact.rs`

## Purpose
This file implements a `ReadExact` future for asynchronously reading an exact number of bytes into a buffer. It ensures the buffer is fully filled or returns an error if an early EOF (end-of-file) occurs. This utility is part of Tokio's asynchronous I/O operations.

---

## Key Components

### 1. **`read_exact` Function**
   - **Role**: Constructs a `ReadExact` future.
   - **Parameters**:
     - `reader`: A mutable reference to an `AsyncRead` type (e.g., a TCP stream).
     - `buf`: A mutable buffer to fill with read bytes.
   - **Returns**: A `ReadExact` future that resolves when the buffer is fully populated or errors on early EOF.

### 2. **`ReadExact` Struct**
   - **Attributes**:
     - `reader`: The source of data (implements `AsyncRead`).
     - `buf`: A `ReadBuf` wrapper to track read progress safely.
     - `_pin`: Ensures the future is `!Unpin` for async safety.
   - **Macro**: `pin_project!` is used to handle pinning for safe async operations.

### 3. **Future Implementation**
   - **`poll` Method**:
     - Repeatedly calls `poll_read` on the underlying reader until the buffer is full.
     - Checks for early EOF by comparing buffer remaining space before and after reads.
     - Returns `Poll::Ready` with the total bytes read on success or an `UnexpectedEof` error.

### 4. **Helper Function**
   - `eof()`: Constructs an `io::Error` for early EOF scenarios.

---

## Integration with the Project
- **Part of Tokio's I/O Utilities**: Works with `AsyncReadExt::read_exact` to provide precise byte-reading functionality.
- **Complementary to Other Futures**: Similar to `read_until` or `read_to_end`, but enforces exact buffer filling instead of variable-length reads.
- **Safety**: Uses `ReadBuf` to manage uninitialized memory safely and `PhantomPinned` to enforce pinning semantics.

---

## Key Differences from Related Code
- Unlike `read_until` (which reads until a delimiter) or `read_to_end` (which reads all bytes), `ReadExact` strictly fills a fixed-size buffer.
- Uses `ReadBuf` for safer buffer management compared to raw byte arrays.

---

## Role in the Project