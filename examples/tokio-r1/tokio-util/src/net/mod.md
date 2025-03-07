# Tokio-util Network Helpers Module (`net/mod.rs`)

## Purpose
This module provides abstractions and utilities for handling TCP, UDP, and Unix socket operations in Tokio. It defines a unified interface for network listeners and enables generic code across different listener types (e.g., TCP and Unix).

## Key Components

### 1. `Listener` Trait
- **Abstraction Layer**: Defines a common interface for listeners like `TcpListener` and `UnixListener`.
- **Associated Types**:
  - `Io`: The async stream type (e.g., `TcpStream`, `UnixStream`).
  - `Addr`: The socket address type (e.g., `std::net::SocketAddr`).
- **Core Methods**:
  - `poll_accept`: Non-blocking poll to accept incoming connections.
  - `accept`: Returns a future (`ListenerAcceptFut`) for async connection acceptance.
  - `local_addr`: Retrieves the listener's bound address.

### 2. `TcpListener` Implementation
- Implements `Listener` for Tokio's `TcpListener`:
  - `Io` is mapped to `TcpStream`.
  - Delegates `poll_accept` and `local_addr` to the underlying `TcpListener` methods.
- Enables TCP listeners to be used polymorphically via the `Listener` trait.

### 3. `ListenerAcceptFut` Future
- A future wrapper for asynchronous connection acceptance.
- Implements `Future` to poll the listener's `poll_accept` method.
- Returned by the `accept` method of the `Listener` trait.

### 4. `Either` Extension
- Extends the `Either` enum (from `crate::either`) to work with listeners:
  - `accept`: Asynchronously accepts connections from either a left or right listener type.
  - `local_addr`: Retrieves the address from either listener variant.
- Allows writing code that operates on multiple listener types without early binding.

## Integration with the Project
- **Unified Listener Interface**: Simplifies code that handles multiple listener types (e.g., TCP and Unix) by abstracting their differences.
- **Platform-Specific Support**: Conditionally includes Unix socket utilities via `#[cfg(unix)] pub mod unix`.
- **Tokio Ecosystem Integration**: Builds on Tokio's core networking types (`TcpListener`, `UnixListener`) to provide reusable utilities in `tokio-util`.

## Role in the Project