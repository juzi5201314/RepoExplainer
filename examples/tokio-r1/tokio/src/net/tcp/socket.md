# Tokio TCP Socket Implementation (`socket.rs`)

## Purpose
The `socket.rs` file provides a low-level TCP socket abstraction (`TcpSocket`) for configuring and managing TCP sockets before they transition into active connections (`TcpStream`) or listeners (`TcpListener`). It bridges OS-level socket configuration with Tokio's async runtime, enabling fine-grained control over socket options not exposed by higher-level APIs.

## Key Components

### 1. **`TcpSocket` Struct**
- **Wraps `socket2::Socket`**: Leverages the `socket2` crate for cross-platform socket operations.
- **Pre-connection/listener State**: Represents an unbound/unconnected socket that can be configured before use.
- **OS-Specific Traits**: Implements `AsRawFd` (Unix) and `AsRawSocket` (Windows) for interoperability.

### 2. **Socket Configuration Methods**
- **Creation**:
  - `new_v4()`/`new_v6()`: Create IPv4/IPv6 sockets with `SOCK_STREAM` type and TCP protocol.
  - Non-blocking setup handled automatically (OS-specific logic).
- **Options**:
  - `set_reuseaddr`, `set_keepalive`, `set_nodelay`, etc.: Configure socket options like `SO_REUSEADDR`, `TCP_NODELAY`.
  - Platform-specific options (e.g., `set_reuseport` on Unix).

### 3. **Conversion Methods**
- **`connect()`**: Converts `TcpSocket` into a connected `TcpStream` (async).
- **`listen()`**: Converts `TcpSocket` into a `TcpListener` for accepting incoming connections.
- **`from_std_stream()`**: Converts a blocking `std::net::TcpStream` into a non-blocking Tokio socket.

### 4. **Cross-Platform Handling**
- Uses `cfg_unix!`/`cfg_windows!` macros to handle OS-specific:
  - Raw socket descriptors (`RawFd` on Unix, `RawSocket` on Windows).
  - Trait implementations (`AsRawFd`, `FromRawSocket`, etc.).

### 5. **Integration with Mio**
- Converts raw sockets into `mio::net::TcpStream`/`TcpListener` for integration with Tokio's async runtime.

## Role in the Project
- **Foundation for TCP Networking**: Serves as the base layer for Tokio's `TcpStream` and `TcpListener`, allowing advanced socket configuration.
- **Flexibility**: Enables use cases requiring custom socket options (e.g., SO_REUSEADDR, TCP_NODELAY) before establishing connections.
- **Cross-Platform Abstraction**: Abstracts OS-specific socket details while exposing a unified API.

---
