# Async Buffered Reading in Tokio

## Purpose
This file defines the `AsyncBufRead` trait, an asynchronous counterpart to `std::io::BufRead`, enabling non-blocking buffered I/O operations in Tokio. It provides a foundation for efficiently reading data streams without blocking threads, integrating with Tokio's task scheduling system.

## Key Components

### 1. `AsyncBufRead` Trait
- **Core Methods**:
  - `poll_fill_buf`: Attempts to return a buffer of available data. Returns `Poll::Pending` if data isn't ready, scheduling a wakeup.
  - `consume`: Marks bytes as consumed after reading, ensuring they aren't reprocessed.
- **Design**: Integrates with Rust's async runtime by using `Poll` and `Context` for cooperative scheduling.

### 2. Implementations
- **Smart Pointers**:
  - `Box<T>`, `&mut T`, and `Pin<P>` delegate calls to their underlying `AsyncBufRead` types using the `deref_async_buf_read!` macro.
- **In-Memory Buffers**:
  - `&[u8]` (byte slices): Directly returns available data; `consume` trims the slice.
  - `io::Cursor<T>`: Wraps synchronous `BufRead` implementations for async compatibility.

### 3. Macro Utilities
- `deref_async_buf_read!`: Simplifies trait delegation for smart pointers, reducing boilerplate code.

## Integration with the Project
- **Buffered I/O Infrastructure**: Serves as the base trait for async buffered readers (e.g., `BufReader`, `BufStream`).
- **Interoperability**: Enables seamless use of buffered operations across Tokio's I/O utilities (e.g., `AsyncReadExt`, `AsyncWrite`).
- **Efficiency**: Reduces syscalls via buffering and supports partial consumption of data.

## Related Context
- Used by components like `BufReader`, `Chain`, and `BufStream` to implement buffered reading.
- Complements `AsyncRead` and `AsyncWrite` traits, forming Tokio's async I/O ecosystem.

---
