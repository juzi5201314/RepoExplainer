# Tokio-Stream TCP Listener Wrapper

## Purpose
This file provides `TcpListenerStream`, a wrapper around Tokio's `TcpListener` that implements the `Stream` trait. Its primary purpose is to enable treating TCP listeners as asynchronous streams of incoming connections, allowing integration with stream combinators and async/await patterns.

## Key Components

### 1. Struct Definition
```rust
pub struct TcpListenerStream {
    inner: TcpListener,
}
```
Wraps a Tokio `TcpListener` while maintaining identical functionality.

### 2. Core Functionality
- **Stream Implementation**: 
  ```rust
  impl Stream for TcpListenerStream {
      type Item = io::Result<TcpStream>;
      fn poll_next(...) -> Poll<Option<...>>
  }
  ```
  Polls the listener for new connections using `poll_accept`, yielding:
  - `Ready(Ok(stream))` for successful connections
  - `Ready(Err(err))` for connection errors
  - `Pending` when waiting for connections

### 3. Conversion Methods
- `new()`: Creates wrapper from existing listener
- `into_inner()`: Recovers original `TcpListener`
- `AsRef/AsMut`: Provides direct access to underlying listener

## Integration with Project
Part of `tokio-stream` crate's network utilities, this wrapper:
1. Bridges Tokio's async I/O primitives with stream abstractions
2. Enables composition with stream combinators (e.g., `chain()` in examples)
3. Supports unified handling of multiple listeners (IPv4/IPv6 shown in example)

## Example Usage
Demonstrates handling dual-stack IPv4/IPv6 servers:
```rust
let ipv4_connections = TcpListenerStream::new(ipv4_listener);
let ipv6_connections = TcpListenerStream::new(ipv6_listener);
let mut connections = ipv4_connections.chain(ipv6_connections);
```
