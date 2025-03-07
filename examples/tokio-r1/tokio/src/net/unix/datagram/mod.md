# Unix Datagram Socket Implementation in Tokio

## Purpose
This file implements Unix domain datagram socket functionality for Tokio's asynchronous runtime. It provides types and methods for creating and managing connectionless, datagram-oriented communication between processes on Unix-like systems.

## Key Components

### 1. Core Structures
- `UnixSocket`: Main socket wrapper around `socket2::Socket` with type checking
- `UnixDatagram`: Async datagram socket type integrated with Tokio's event loop

### 2. Socket Management
- `new_datagram()`: Creates new DGRAM-type sockets using `socket(2)` system call
- Type validation: Methods like `datagram()` and `listen()` enforce socket type constraints
- Conversion: `from_std()` bridges standard library sockets to Tokio's async system

### 3. Async Integration
- Uses `PollEvented` from Tokio's I/O utilities for async readiness notification
- Implements non-blocking I/O operations through mio integration

### 4. Unix-specific Features
- `SocketAddr`: Unix domain socket address handling
- `UCred`: Process credential retrieval (PID, UID, GID)
- Pipe support through separate `pipe` module

### 5. Error Handling
- Enforces proper socket type usage (e.g., preventing listen() on DGRAM sockets)
- Converts system errors to Rust's `io::Error` format

## Project Context
This file is part of Tokio's Unix-specific networking implementation. It works with:
- `stream.rs` for connection-oriented sockets
- `listener.rs` for passive socket creation
- `split.rs` for read/write handle separation

The implementation sits between the raw socket2 library and Tokio's async abstractions, providing:
- Type-safe socket creation
- Async readiness notification
- Error conversion
- Standard library interoperability
