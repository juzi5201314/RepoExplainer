# Unix Domain Socket Address Wrapper (`socketaddr.rs`)

## Purpose
This file provides a Tokio-specific wrapper around the standard library's Unix domain socket address (`std::os::unix::net::SocketAddr`). It enables seamless integration with Tokio's asynchronous networking components while maintaining interoperability with the standard library.

## Key Components

### `SocketAddr` Struct
- A thin tuple struct wrapping `std::os::unix::net::SocketAddr`.
- **Visibility**: `pub(super)` restricts direct instantiation to internal Tokio modules.
- **Methods**:
  - `is_unnamed()`: Checks if the socket is unnamed (abstract/pathless).
  - `as_pathname()`: Retrieves the filesystem path for path-based sockets.

### Trait Implementations
1. **`From` Conversions**:
   - Bidirectional conversion between Tokio's `SocketAddr` and the standard library's version.
   - Enables transparent interoperability between Tokio and non-Tokio code.

2. **`Debug` Formatting**:
   - Delegates to the underlying standard library implementation for consistent debugging output.

## Integration with Project
- Used in Tokio's Unix domain socket implementations (`UnixStream`, `UnixDatagram`) for methods like `local_addr()`.
- Facilitates address handling in async operations while maintaining compatibility with synchronous `std` types.
- Appears in conversion utilities (e.g., `convert_address`) for lower-level socket operations using `socket2` crate types.

## Example Usage Context
```rust
// In Tokio APIs like UnixDatagram::local_addr()
let socket = UnixDatagram::unbound()?;
let addr: SocketAddr = socket.local_addr()?;
if addr.is_unnamed() {
    // Handle abstract socket
}
```
