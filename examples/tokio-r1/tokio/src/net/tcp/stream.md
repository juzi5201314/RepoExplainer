# Tokio TCP Stream Implementation

## Purpose
The `stream.rs` file implements the asynchronous `TcpStream` type for Tokio, providing non-blocking TCP network communication between local and remote sockets. It serves as the core component for handling TCP connections in Tokio's networking stack.

## Key Components

### 1. TcpStream Struct
- **Wrapper**: Contains a `PollEvented<mio::net::TcpStream>` for integrating with Tokio's event loop.
- **Features**:
  - Async connection establishment
  - Read/write operations with readiness polling
  - Socket option management (nodelay, ttl, linger)
  - Splitting into read/write halves

### 2. Connection Management
- **Async Connect**: `connect()` resolves addresses and establishes connections
- **MIO Integration**: Uses mio's TCP stream with Tokio's reactor
- **Platform Interop**: Conversion methods between Tokio and stdlib TCP streams (`from_std`, `into_std`)

### 3. Async I/O Implementation
- **AsyncRead/AsyncWrite**: Implements Tokio's async traits using:
  - `poll_read()`: Non-blocking read with buffer management
  - `poll_write()`: Non-blocking write operations
  - Vectored I/O support (`read_vectored`, `write_vectored`)

### 4. Readiness API
- **Event-Driven**: Methods like `ready()`, `readable()`, and `writable()` for async readiness waiting
- **Poll-Based**: Low-level `poll_read_ready()` and `poll_write_ready()` for direct context polling

### 5. Advanced Features
- **Socket Options**: Configuration of TCP_NODELAY, IP_TTL, SO_LINGER
- **Split API**: `split()` and `into_split()` for concurrent read/write handling
- **Peek Operations**: `poll_peek()` for viewing data without consumption

## Project Integration
- **Network Stack Core**: Forms foundation for higher-level TCP protocols
- **Runtime Integration**: Works with Tokio's executor and reactor
- **Interoperability**: Bridges between async Tokio API and synchronous stdlib types
- **Modular Design**: Complements `TcpListener` and socket types in networking module

## Key Methods
```rust
// Core functionality examples
TcpStream::connect() // Async connection
stream.readable().await // Wait for read readiness
stream.try_write() // Non-blocking write attempt
stream.split() // Concurrent access
stream.set_nodelay() // Socket optimization
```

## Platform Handling
- **Conditional Compilation**: WASI-specific exclusions
- **OS-Specific Traits**: Implements `AsRawFd`/`AsRawSocket` for Unix/Windows

---
