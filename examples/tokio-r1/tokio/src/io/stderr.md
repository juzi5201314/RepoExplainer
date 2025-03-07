# Tokio Standard Error (stderr) Implementation

## Purpose
This file provides an asynchronous interface to the standard error stream (stderr) in Tokio. It enables non-blocking writes to stderr within asynchronous Rust applications while handling platform-specific behaviors (particularly Windows UTF-8 boundary splitting).

## Key Components

### `Stderr` Struct
- **Wraps**: `SplitByUtf8BoundaryIfWindows<Blocking<std::io::Stderr>>`
- **Purpose**: 
  - Provides thread-safe async writes to stderr.
  - Ensures UTF-8 boundaries are respected on Windows to prevent garbled output.
  - Uses `Blocking` to bridge synchronous I/O with Tokio's async runtime.

### `stderr()` Constructor
- Creates a `Stderr` instance with:
  1. The standard `std::io::stderr` handle.
  2. A `Blocking` wrapper to execute I/O in a thread pool (prevents runtime stalls).
  3. `SplitByUtf8BoundaryIfWindows` for Windows-specific UTF-8 safety.

### Platform-Specific Implementations
- **Unix**: Implements `AsRawFd`/`AsFd` for file descriptor access.
- **Windows**: Implements `AsRawHandle`/`AsHandle` for handle access.

### Async Integration
- Implements `AsyncWrite` trait with:
  - `poll_write`: Delegates to inner `SplitByUtf8BoundaryIfWindows`.
  - `poll_flush`/`poll_shutdown`: Forward to underlying I/O resource.

## Relationship to Project
- Part of Tokio's I/O utilities alongside `stdout.rs`.
- Works with `blocking.rs` and `stdio_common` modules to handle cross-platform quirks.
- Enables async/await patterns for error stream interactions (e.g., logging).

## Notable Design Choices
- **Concurrency Warning**: Explicitly documents that `write_all` might interleave output across threads.
- **Windows Special Handling**: UTF-8 boundary splitting avoids partial character writes in console environments.

---
