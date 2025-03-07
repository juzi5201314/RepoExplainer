# Tokio Unix Stream Split Implementation

## Purpose
This module provides zero-cost splitting of a Unix domain socket stream (`UnixStream`) into separate read and write halves. It enables concurrent read/write operations without synchronization overhead by leveraging Rust's borrowing rules.

## Key Components

### 1. Core Structures
- **`ReadHalf<'a>`**: Borrowed read half implementing `AsyncRead`
- **`WriteHalf<'a>`**: Borrowed write half implementing `AsyncWrite`

Both contain a reference to the original `UnixStream`:
```rust
pub struct ReadHalf<'a>(&'a UnixStream);
pub struct WriteHalf<'a>(&'a UnixStream);
```

### 2. Splitting Mechanism
The `split` function creates tuple of halves:
```rust
pub(crate) fn split(stream: &mut UnixStream) -> (ReadHalf<'_>, WriteHalf<'_>) {
    (ReadHalf(stream), WriteHalf(stream))
}
```

### 3. Key Functionality
**ReadHalf Features:**
- Async readiness notification (`ready()`, `readable()`)
- Non-blocking reads (`try_read()`, `try_read_buf()`, `try_read_vectored()`)
- Socket address inspection (`peer_addr()`, `local_addr()`)

**WriteHalf Features:**
- Async write readiness (`ready()`, `writable()`)
- Non-blocking writes (`try_write()`, `try_write_vectored()`)
- Proper stream shutdown handling in `poll_shutdown()`

### 4. Async Trait Implementations
- `AsyncRead` for `ReadHalf` delegates to `UnixStream::poll_read_priv`
- `AsyncWrite` for `WriteHalf` delegates to `UnixStream::poll_write_priv` and handles write shutdown

## Design Advantages
1. **Zero-Cost Abstraction**: Uses Rust references instead of Arc/Mutex
2. **Type Safety**: Enforces read/write separation at compile time
3. **API Consistency**: Mirrors TCP stream splitting interface
4. **Conditional Features**: `try_read_buf` only compiled with `io_util` feature

## Integration with Tokio
- Part of Tokio's UNIX domain socket implementation
- Complements other split implementations (TCP, UDP)
- Used by higher-level components needing concurrent IO on Unix streams
- Integrates with Tokio's async runtime through `Interest`/`Ready` system

## Relationship to Other Components
- Shares patterns with `tcp::split` and `udp::split` modules
- Builds on `PollEvented` for async IO readiness notifications
- Complements owned splitting variant (`into_split`) elsewhere in codebase
