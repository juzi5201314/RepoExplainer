# Tokio AsyncWrite Trait Implementation

## Purpose
This file defines the core `AsyncWrite` trait and its implementations, providing asynchronous non-blocking write capabilities for Tokio's I/O system. It serves as the async counterpart to `std::io::Write`, enabling integration with Tokio's event-driven runtime.

## Key Components

### 1. AsyncWrite Trait
- **Core Methods**:
  - `poll_write`: Attempts to write bytes, returning readiness status (Ready/Pending) or errors.
  - `poll_flush`: Ensures buffered data reaches its destination asynchronously.
  - `poll_shutdown`: Gracefully terminates writing while ensuring final data flushes.
- **Vectored Writes**:
  - `poll_write_vectored`: Scatter/gather I/O support (default: uses first non-empty buffer).
  - `is_write_vectored`: Indicates optimized vectored write support.

### 2. Implementations
- **Smart Pointers**:
  - `Box<T>`, `&mut T`, and `Pin<P>` forward calls to their contained `AsyncWrite` implementations using a `deref_async_write` macro.
- **In-Memory Writers**:
  - `Vec<u8>`: Immediate writes with automatic buffer growth.
  - `io::Cursor` variants: Implement async writes for different buffer types (slices, `Vec<u8>`, `Box<[u8]>`).

### 3. Design Features
- **Non-Blocking Semantics**: Methods return `Poll` to integrate with Tokio's task scheduling.
- **Backpressure Handling**: `Poll::Pending` triggers task wakeups when resources become available.
- **Error Propagation**: Mirrors standard I/O error handling in async context.

## Integration with Project
- **Foundation for Async I/O**: Works with `AsyncRead` to form Tokio's core I/O primitives.
- **Interoperability**: Enables async operations with TCP streams, files, pipes, and in-memory buffers.
- **Utilities**: Used by `AsyncWriteExt` extension methods and higher-level components like `copy` for data transfer between async readers/writers.
