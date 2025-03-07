# Tokio Vectored Write Future Implementation

## Purpose
This file implements an asynchronous vectored write operation for Tokio's I/O system. It provides a `WriteVectored` future that writes multiple buffers (via `IoSlice`) to an `AsyncWrite` implementer in a single operation, supporting scatter-gather I/O patterns efficiently.

## Key Components

### 1. WriteVectored Struct
- **Pinned Future**: Uses `pin_project!` macro to create a `!Unpin` type
- **Fields**:
  - `writer`: Mutable reference to an `AsyncWrite` implementer
  - `bufs`: Slice of `IoSlice` buffers to write
  - `_pin`: PhantomPinned marker for pinning guarantees

### 2. Constructor Function
- `write_vectored()`: Creates a new `WriteVectored` future
- Enforces `Unpin` requirement on writer for safe movement between memory locations

### 3. Future Implementation
- `poll()` method delegates to underlying writer's `poll_write_vectored`
- Returns `Poll::Ready` with bytes written count or pending status
- Maintains zero-cost abstraction by directly using writer's capabilities

## Integration with Tokio
- Part of Tokio's I/O utility module
- Complements other write operations (`write()`, `write_all()`, `write_buf()`)
- Implements standard Future pattern for async/await compatibility
- Works with Tokio's async I/O ecosystem through `AsyncWrite` trait

## Performance Considerations
- Enables efficient scatter-gather I/O operations
- Avoids unnecessary buffer copies by using `IoSlice`
- Directly leverages OS-level vectored I/O capabilities where available
