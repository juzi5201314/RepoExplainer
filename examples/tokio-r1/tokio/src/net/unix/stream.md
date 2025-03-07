# Unix Stream Implementation in Tokio

## Purpose
This file (`stream.rs`) implements an asynchronous Unix domain socket stream for Tokio, providing non-blocking I/O operations for inter-process communication (IPC) on Unix-based systems. It enables bidirectional data flow between connected sockets with async/await support.

## Key Components

### 1. **UnixStream Structure**
- **Core Type**: Wraps a `mio::net::UnixStream` with Tokio's `PollEvented` for event polling.
- **Async Capabilities**: Implements `AsyncRead` and `AsyncWrite` traits for seamless integration with Tokio's runtime.

### 2. **Connection Management**
- **`connect()`**: Establishes a connection to a Unix socket path, handling abstract addresses on Linux/Android.
- **`pair()`**: Creates an unnamed socket pair for local communication.
- **OS-Specific Handling**: Abstracts Linux/Android vs. other Unix-like OS differences in socket addressing.

### 3. **I/O Operations**
- **Async Read/Write**: Methods like `readable()`, `writable()`, and `ready()` wait for socket readiness.
- **Non-Blocking Attempts**: `try_read()`, `try_write()`, and their vectored variants perform immediate I/O without blocking.
- **Buffer Management**: Supports `bytes::BufMut` for efficient buffer handling in `try_read_buf`.

### 4. **Splitting Streams**
- **`split()`**: Borrows the stream into read/write halves for concurrent access.
- **`into_split()`**: Creates owned halves that can move across tasks (heap-allocated).

### 5. **Conversion Utilities**
- **`from_std()`**: Converts a blocking stdlib `UnixStream` to async Tokio stream (requires non-blocking mode).
- **`into_std()`**: Converts back to a stdlib stream, preserving file descriptor.

### 6. **Ancillary Features**
- **Socket Metadata**: `local_addr()`, `peer_addr()`, and `peer_cred()` for connection details.
- **Error Handling**: `take_error()` retrieves socket-level errors.
- **Shutdown**: Graceful connection termination via `shutdown_std()`.

## Integration with Tokio
- **Event Loop**: Uses `PollEvented` to register with Tokio's reactor for I/O readiness notifications.
- **Async Traits**: Implements `AsyncRead`/`AsyncWrite` to work with Tokio's runtime and combinators.
- **Feature Flags**: Conditionally includes utilities like `bytes` support via `cfg_io_util!`.

## Example Flow
1. **Connect**: `UnixStream::connect("path.sock").await`
2. **Async Read**: `stream.readable().await` → `try_read()`
3. **Async Write**: `stream.writable().await` → `try_write()`
4. **Shutdown**: `stream.shutdown(Shutdown::Write)`

## Role in Project