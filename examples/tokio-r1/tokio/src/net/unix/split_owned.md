# UnixStream Owned Split Implementation

## Purpose
This module provides owned split functionality for Unix domain sockets (`UnixStream`), allowing it to be divided into two independent halves: `OwnedReadHalf` and `OwnedWriteHalf`. These halves can be used concurrently across tasks with zero runtime overhead, enforcing safety through Rust's type system.

## Key Components

### 1. Struct Definitions
- **`OwnedReadHalf`**: 
  - Contains an `Arc<UnixStream>` to share ownership of the underlying socket.
  - Implements `AsyncRead` for non-blocking reads.
- **`OwnedWriteHalf`**:
  - Also wraps an `Arc<UnixStream>`.
  - Includes a `shutdown_on_drop` flag to control write-side shutdown behavior.
  - Implements `AsyncWrite` for non-blocking writes and automatically shuts down writes on drop unless disabled.

### 2. Core Functions
- **`split_owned(stream: UnixStream)`**:
  - Splits a `UnixStream` into owned read/write halves using `Arc` for shared ownership.
- **`reunite()`**:
  - Recombines read/write halves back into the original `UnixStream` if they originated from the same split operation. Returns `ReuniteError` on mismatch.

### 3. Error Handling
- **`ReuniteError`**:
  - Indicates an attempt to reunite halves from different sockets.
  - Implements `std::error::Error` and provides a descriptive error message.

### 4. Method Delegation
Both halves delegate I/O operations to the underlying `UnixStream`:
- Read methods (`try_read`, `try_read_buf`, `poll_read`) call into the shared `UnixStream`.
- Write methods (`try_write`, `poll_write`, `poll_shutdown`) similarly delegate to the socket.
- Additional utilities like `peer_addr()` and `local_addr()` provide socket metadata.

### 5. Resource Management
- **Drop Behavior**:
  - `OwnedWriteHalf` automatically shuts down the write side of the socket when dropped (unless `forget()` is called).
  - Uses `shutdown_std(Shutdown::Write)` for graceful termination.

## Integration with the Project
- Part of Tokio's Unix domain socket implementation, mirroring similar split functionality for TCP streams.
- Enables concurrent read/write operations across asynchronous tasks without locks or runtime checks.
- Complements borrowed splitting (via `split()`) by providing owned halves with `'static` lifetimes, useful for scenarios requiring independent ownership.

## Role in the Project