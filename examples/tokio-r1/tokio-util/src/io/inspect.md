# Code Explanation: `tokio-util/src/io/inspect.rs`

## Purpose
This file provides two async I/O adapters, `InspectReader` and `InspectWriter`, designed to inspect data during read/write operations in Tokio. These adapters allow users to execute custom logic (e.g., logging, hashing) on the data being processed without interrupting the I/O flow.

## Key Components

### 1. `InspectReader`
- **Structure**: Wraps an `AsyncRead` type `R` and a closure `F`.
- **Functionality**:
  - Overrides `poll_read` to capture newly read data after delegating to the inner reader.
  - Invokes the closure `F` on the newly read bytes (using `buf.filled()` to track changes).
  - Implements `AsyncWrite` if the inner reader supports it, passing through write operations.

### 2. `InspectWriter`
- **Structure**: Wraps an `AsyncWrite` type `W` and a closure `F`.
- **Functionality**:
  - Overrides `poll_write` and `poll_write_vectored` to invoke `F` on successfully written data.
  - Handles vectored writes by iterating over buffers and invoking `F` for each non-empty slice.
  - Implements `AsyncRead` if the inner writer supports it, delegating read operations.

### Shared Traits
- **`into_inner()`**: Returns the wrapped I/O object, allowing reuse after inspection.
- **Pin Projection**: Uses `pin_project!` macro to safely handle pinned fields in async contexts.

## Integration with the Project
- Part of `tokio-util`, a utilities crate complementing Tokio's core async I/O.
- Enables middleware-like behavior for async streams (e.g., monitoring, transformation).
- Composes with other Tokio adapters (e.g., `AsyncReadExt`, `AsyncWriteExt`) for modular data processing.

## Related Context
The code follows patterns seen in other Tokio utilities (e.g., `read_until_internal`, `read_line_internal`), where polling methods delegate to inner I/O objects while injecting custom logic. The use of `ReadBuf` and `poll_read` aligns with Tokio's async I/O conventions.

---
