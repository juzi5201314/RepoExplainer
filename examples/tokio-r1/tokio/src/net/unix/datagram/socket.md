# Unix Datagram Socket Implementation in Tokio

## Purpose
This file (`tokio/src/net/unix/datagram/socket.rs`) implements an asynchronous Unix domain datagram socket (`UnixDatagram`) for Tokio. It provides non-blocking I/O operations for connectionless, message-oriented communication between processes on the same host.

## Key Components

### 1. **Core Struct: `UnixDatagram`**
- Wraps a `mio::net::UnixDatagram` with Tokio's `PollEvented` for async event polling.
- Supports both named (filesystem-bound) and unnamed sockets.
- Thread-safe by design (methods take `&self`).

### 2. **Key Functionality**
- **Socket Creation**:
  - `bind()`: Binds to a filesystem path.
  - `pair()`: Creates an unnamed socket pair.
  - `from_std()`: Converts a standard library socket to Tokio's async version.
- **Async I/O Operations**:
  - `send()`, `recv()`: Connected operations.
  - `send_to()`, `recv_from()`: Unconnected operations with address specification.
  - Non-blocking variants (`try_send()`, `try_recv_from()`) for direct use with readiness checks.
- **Readiness Handling**:
  - `ready()`, `writable()`, `readable()`: Async methods to wait for I/O readiness.
  - `poll_send_ready()`, `poll_recv_ready()`: Lower-level polling for futures integration.

### 3. **Advanced Features**
- **Buffer Utilities**:
  - `try_recv_buf_from()`, `recv_buf_from()`: Work with uninitialized buffers using `bytes::BufMut`.
- **Socket Metadata**:
  - `local_addr()`, `peer_addr()`: Query socket addresses.
  - `take_error()`: Retrieve pending socket errors.
- **Shutdown**:
  - `shutdown()`: Gracefully close read/write halves.

### 4. **Integration with Tokio Runtime**
- Uses `PollEvented` to register with Tokio's reactor for I/O event notifications.
- Implements cancel-safe async methods using `Interest` (READABLE/WRITABLE states).

## Example Usage
```rust
// Named sockets
let tx = UnixDatagram::bind("/tmp/sock.tx")?;
tx.send_to(b"data", "/tmp/sock.rx").await?;

// Socket pairs
let (sock1, sock2) = UnixDatagram::pair()?;
sock1.send(b"hello").await?;
let mut buf = [0; 1024];
let len = sock2.recv(&mut buf).await?;
```

## Relationship to Project
This file is part of Tokio's Unix domain socket implementation, complementing `UnixStream` (connection-oriented) and `UnixListener`. It enables async message-passing patterns in Unix-based systems, critical for:
- Local inter-process communication (IPC)
- High-performance services where TCP overhead is undesirable
- Datagram-based protocols requiring async I/O
