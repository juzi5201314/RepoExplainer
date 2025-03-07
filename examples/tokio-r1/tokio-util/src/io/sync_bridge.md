# SyncIoBridge in tokio-util

## Purpose
The `SyncIoBridge` struct provides a compatibility layer to use Tokio's asynchronous I/O types (`AsyncRead`, `AsyncWrite`, etc.) in synchronous contexts by blocking the current thread. It bridges between asynchronous and synchronous I/O operations while emphasizing proper usage patterns to avoid runtime inefficiencies.

## Key Components

### Struct Definition
```rust
pub struct SyncIoBridge<T> {
    src: T,  // Wrapped async I/O object
    rt: tokio::runtime::Handle  // Tokio runtime handle
}
```

### Core Implementations
Implements synchronous I/O traits by wrapping async operations with blocking calls:
- **`Read`/`Write`/`Seek`/`BufRead`**: Uses `rt.block_on()` to execute async operations synchronously
- **Vectored Write Support**: `is_write_vectored()` checks underlying async writer capabilities
- **Graceful Shutdown**: `shutdown()` ensures proper writer termination

### Construction Methods
- `new()`: Captures current runtime handle (requires Tokio context)
- `new_with_handle()`: Allows explicit runtime handle specification

## Important Considerations
1. **Thread Blocking**: Designed to be used within `spawn_blocking` to avoid starving async runtime
2. **Performance Tradeoffs**:
   - Uses OS thread per operation (resource-intensive)
   - May cause thread pool saturation if overused
3. **Alternatives Encouraged**: Provides extensive documentation with async-first patterns for common use cases (hashing, compression, JSON parsing)

## Project Role
This utility enables interoperability with synchronous libraries in async contexts when absolutely necessary, while actively discouraging misuse through detailed documentation of better async-native patterns. It serves as an escape hatch in Tokio's ecosystem for legacy integration scenarios.
