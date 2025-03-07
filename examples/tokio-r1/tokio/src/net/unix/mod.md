# Unix Network Module in Tokio

## Purpose
This module (`tokio/src/net/unix/mod.rs`) serves as the core implementation of Unix-specific networking components for Tokio's asynchronous runtime. It provides abstractions for working with Unix domain sockets, pipes, and process credentials in a platform-specific manner.

## Key Components

### Core Types
- **UnixStream**: Async Unix domain stream socket (TCP-like)
- **UnixListener**: Unix domain socket listener (server side)
- **UnixDatagram**: Unix domain datagram socket (UDP-like, hidden from docs)
- **UCred**: Structure for handling peer process credentials
- **SocketAddr**: Unix-specific socket address (path-based)

### Splitting Mechanisms
- `split` module: Borrowed read/write halves (`ReadHalf`, `WriteHalf`)
- `split_owned` module: Owned variants with lifetime management (`OwnedReadHalf`, `OwnedWriteHalf`)

### Platform-Specific Features
- **ucred**: User credential handling for peer processes
- **pipe**: Unix named pipe (FIFO) support
- Type aliases for Unix ID types (`uid_t`, `gid_t`, `pid_t`)

## Implementation Details
- Uses `pub(crate)` visibility to expose components internally while maintaining clean public API
- Contains hidden `datagram` module for internal Unix datagram implementation
- Provides socket address handling through `socketaddr` module
- Integrates with Tokio's async I/O system through stream/listener implementations

## Relationship to Project
- Mirrors TCP networking architecture but for Unix domain sockets
- Enables cross-platform networking code with Unix-specific optimizations
- Forms foundation for inter-process communication (IPC) in Tokio applications
- Works with other Tokio components through standard AsyncRead/AsyncWrite traits
