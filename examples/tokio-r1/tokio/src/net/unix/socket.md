# Unix Socket Configuration in Tokio

## Purpose
The `socket.rs` file provides a flexible Unix socket configuration API for Tokio's asynchronous networking. It enables advanced socket setup (options, binding) before converting into specific socket types (`UnixStream`, `UnixDatagram`, `UnixListener`).

## Key Components

### 1. `UnixSocket` Struct
- **Wrapper**: Contains a `socket2::Socket` for cross-platform abstraction
- **Functionality**:
  - Create stream/datagram sockets via `new_stream()`/`new_datagram()`
  - Bind sockets to paths with `bind()`
  - Convert to final socket types via `listen()`, `connect()`, and `datagram()`

### 2. Socket Creation
- **OS Integration**: Uses `socket2` crate for system calls
- **Non-blocking Setup**:
  ```rust
  #[cfg(unix_platforms)]
  let ty = ty.nonblocking(); // Built-in in socket2
  #[cfg(other_platforms)]
  inner.set_nonblocking(true); // Manual fallback
  ```

### 3. Conversion Methods
| Method        | Output Type      | Key Operation           |
|---------------|------------------|-------------------------|
| `listen()`    | `UnixListener`   | Calls `listen(2)` + mio integration |
| `connect()`   | `UnixStream`     | Async connection with EINPROGRESS handling |
| `datagram()`  | `UnixDatagram`   | Direct conversion to datagram socket |

### 4. File Descriptor Handling
Implements standard traits for FD interoperability:
- `AsRawFd`/`AsFd` for borrowing
- `FromRawFd`/`IntoRawFd` for safe ownership transfers

## Project Integration
- **Foundation Layer**: Sits below higher-level types like `UnixStream`
- **Configuration Bridge**: Allows socket tuning before async operations
- **Unix Specific**: Part of Tokio's Unix-specific networking module (`cfg_net_unix!`)

## Example Flow
```rust
let socket = UnixSocket::new_stream()?;
socket.bind("/tmp/sock")?;
let listener = socket.listen(128)?; // Now usable with async accept()
```

This file provides low-level socket configuration capabilities for Unix domain sockets in Tokio's async runtime.  