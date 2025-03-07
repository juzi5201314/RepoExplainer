# BufWriter in Tokio's Async I/O Utilities

## Purpose
The `BufWriter` struct provides buffered asynchronous writing by wrapping an underlying writer and batching small writes into larger, more efficient operations. It reduces the overhead of frequent syscalls for small writes, improving performance in scenarios like network communication or file I/O with repetitive small payloads.

## Key Components

### Struct Fields
- **`inner: W`**: The underlying async writer (e.g., TCP stream, file).
- **`buf: Vec<u8>`**: In-memory buffer storing data before flushing.
- **`written: usize`**: Tracks bytes already written to `inner` during flushing.
- **`seek_state: SeekState`**: Manages seek operations to ensure buffer consistency.

### Core Methods
- **`new()`/`with_capacity()`**: Constructors initialize the buffer with default/specified sizes.
- **`flush_buf()`**: Asynchronously writes buffered data to `inner`, handles partial writes/errors.
- **`poll_write()`**: Buffers data or directly writes large chunks to `inner`.
- **`poll_write_vectored()`**: Optimizes scattered writes using `IoSlice`, respecting buffer limits.
- **AsyncSeek Integration**: Flushes buffer before seeking to maintain write consistency.

## Implementation Details

### AsyncWrite Integration
- Buffers small writes (`buf`), flushes when full.
- Directly passes large writes (> buffer capacity) to `inner`.
- Implements vectored writes with fallback logic for non-vectored writers.

### Seek Handling
- **`start_seek()`/`poll_complete()`**: Ensures buffer is flushed before seeking to prevent data misalignment.
- Uses `SeekState` to track pending seek operations.

### Passthrough Reads
- Delegates `AsyncRead`/`AsyncBufRead` calls to `inner`, as buffering only affects writes.

## Integration with Project
- Part of Tokio's `io-util` module, complementing `BufReader` and other I/O utilities.
- Works with Tokio's async traits (`AsyncWrite`, `AsyncSeek`) to enable efficient I/O in async runtimes.
- Used in scenarios requiring batched writes (e.g., logging, network protocols).

---
