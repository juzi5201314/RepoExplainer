# Unix Domain Socket Listener Implementation

## Purpose
This file provides a trait implementation to adapt Tokio's `UnixListener` into a unified `Listener` abstraction, enabling consistent async network listener handling across different transport types (TCP/UDP/Unix) in the tokio-util crate.

## Key Components

### `Listener` Trait Implementation
```rust
impl Listener for tokio::net::UnixListener {
    type Io = tokio::net::UnixStream;
    type Addr = tokio::net::unix::SocketAddr;
    
    fn poll_accept(&mut self, cx: &mut Context<'_>) -> Poll<Result<(Self::Io, Self::Addr)>> {
        Self::poll_accept(self, cx)
    }
    
    fn local_addr(&self) -> Result<Self::Addr> {
        self.local_addr().map(Into::into)
    }
}
```
- **Associated Types**:  
  - `Io`: Specifies `UnixStream` as the connection type
  - `Addr`: Uses Unix-specific `SocketAddr` for endpoint addresses
- **Core Methods**:  
  - `poll_accept`: Delegates to Tokio's native async accept mechanism
  - `local_addr`: Wraps the underlying listener's address retrieval

## Integration with Project
- Part of a cross-protocol abstraction layer in `tokio-util/src/net`
- Works alongside TCP/UDP implementations using the same `Listener` trait interface
- Enables generic network server patterns through unified Stream-based API
- Supports conversion between Tokio and standard library socket types

## Relationship to Context
- Mirrors the `Listener` implementation pattern used for `TcpListener`
- Complements other Unix socket utilities (Datagram, Stream wrappers)
- Forms part of the crate's strategy for protocol-agnostic network programming
