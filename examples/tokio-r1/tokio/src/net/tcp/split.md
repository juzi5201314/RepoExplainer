# Tokio TCP Stream Split Implementation

## Purpose
This file provides a zero-overhead mechanism to split a `TcpStream` into separate `ReadHalf` and `WriteHalf` components, enabling concurrent read/write operations while enforcing type-level safety. It implements asynchronous I/O traits (`AsyncRead`/`AsyncWrite`) for each half to work with Tokio's runtime.

## Key Components

### 1. Core Structs
- **`ReadHalf<'a>`**: Borrowed read half of a TCP stream with:
  - Peeking/reading methods (`poll_peek`, `peek`, `try_read`)
  - Readiness checking (`ready()`, `readable()`)
  - Address inspection (`peer_addr()`, `local_addr()`)

- **`WriteHalf<'a>`**: Borrowed write half of a TCP stream with:
  - Writing methods (`try_write`, `try_write_vectored`)
  - Write readiness checking (`writable()`)
  - Proper stream shutdown handling

### 2. Split Mechanism
- **`split()` function**: Takes a `&mut TcpStream` and returns tuple `(ReadHalf, WriteHalf)`
- Uses shared references to the original stream with no allocation
- Enables simultaneous access through Rust's borrow checker guarantees

### 3. Trait Implementations
- **`AsyncRead` for `ReadHalf`**:
  - Delegates to internal `poll_read_priv` on `TcpStream`
- **`AsyncWrite` for `WriteHalf`**:
  - Implements vectored writes and proper shutdown
  - Uses `poll_write_priv` internally

### 4. Key Features
- **Zero-cost abstraction**: No additional allocation compared to generic splits
- **Cancel safety**: All async methods properly handle task cancellation
- **Buffer utilities**: Integration with `bytes::BufMut` via feature flags

## Integration with Tokio
- Part of Tokio's TCP networking stack
- Used by `TcpStream::split()` method
- Enables patterns like:
  - Concurrent reading/writing across tasks
  - Separate ownership of read/write operations
  - Efficient integration with Tokio's I/O utilities

## Comparison to Alternatives
- Specialized for TCP streams vs generic `AsyncRead+AsyncWrite` splits
- Avoids runtime costs of `Arc`/`Mutex` used in owned split variants
- Maintains direct access to TCP-specific features (peeking, shutdown semantics)
