# Tokio UDP Socket Implementation (`udp.rs`)

## Purpose
This file provides an asynchronous UDP socket implementation for Tokio, enabling non-blocking, connectionless communication. It wraps mio's UDP socket with Tokio's async runtime, supporting both one-to-many (unconnected) and one-to-one (connected) communication patterns.

## Key Components

### 1. **`UdpSocket` Struct**
- **Core Type**: Wraps `PollEvented<mio::net::UdpSocket>` to integrate with Tokio's event loop.
- **Thread Safety**: Designed for shared ownership via `Arc<UdpSocket>` (no `split` method needed).

### 2. **Core Methods**
- **Binding/Connecting**:
  - `bind()`: Creates a UDP socket bound to a specific address.
  - `connect()`: Associates the socket with a remote address for `send`/`recv`.
- **I/O Operations**:
  - Async methods: `send()`, `recv()`, `send_to()`, `recv_from()`.
  - Non-blocking "try" variants: `try_send()`, `try_recv()`, etc.
  - Buffer utilities: `recv_buf()`, `try_recv_buf_from()` (with `bytes::BufMut` support).
- **Readiness API**:
  - `ready()`, `writable()`, `readable()`: Wait for socket readiness.
  - `poll_send_ready()`, `poll_recv_ready()`: Poll-based readiness checks.

### 3. **Socket Configuration**
- **Options**: Methods for `SO_BROADCAST`, `IP_MULTICAST_LOOP`, `IP_TTL`, etc.
- **Platform-Specific Logic**: 
  - Conversion to/from `std::net::UdpSocket` (OS-specific `IntoRawFd`/`FromRawSocket`).
  - Multicast support (`join_multicast_v4`, `leave_multicast_v6`).

### 4. **Advanced Features**
- **Zero-Copy Operations**: `try_recv_buf` and `recv_buf` for buffer management.
- **Low-Level Access**: `try_io()` and `async_io()` for custom I/O integration.

## Usage Patterns
- **One-to-Many**: Use `bind()` + `send_to()`/`recv_from()` for unconnected communication.
- **One-to-One**: Use `connect()` + `send()`/`recv()` for connected communication.
- **Concurrency**: Shared `Arc<UdpSocket>` allows simultaneous sends/receives across tasks.

## Integration with Tokio
- Leverages `PollEvented` to bridge mio's event-driven I/O with Tokio's async runtime.
- Uses `Interest` and `Ready` types to manage I/O readiness notifications.
- Supports cancellation safety for async operations (e.g., `send`/`recv` in `tokio::select!`).

## Examples (From Docs)
```rust
// Echo server (one-to-many)
let sock = UdpSocket::bind("0.0.0.0:8080").await?;
loop {
    let (len, addr) = sock.recv_from(&mut buf).await?;
    sock.send_to(&buf[..len], addr).await?;
}

// Connected client (one-to-one)
sock.connect("127.0.0.1:8081").await?;
let len = sock.recv(&mut buf).await?;
sock.send(&buf[..len]).await?;
```

## Role in the Project