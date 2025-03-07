# Unix Domain Socket Listener Implementation in Tokio

## Purpose
This file implements an asynchronous Unix domain socket listener (`UnixListener`) for Tokio, enabling non-blocking IPC (Inter-Process Communication) on Unix-like systems. It provides server-side functionality to accept incoming connections from Unix sockets.

## Key Components

### 1. Core Structure
- `UnixListener`: Main struct wrapping a `mio::net::UnixListener` with Tokio's event polling
- Contains a `PollEvented` I/O resource for async event notification

### 2. Key Functionality
- **Binding**: 
  - `bind()`: Creates listener bound to filesystem path or abstract address (Linux/Android)
  - Handles OS-specific socket address types
- **Conversion**:
  - `from_std()`: Converts blocking stdlib listener to async Tokio listener
  - `into_std()`: Reverse conversion for interoperability
- **Connection Handling**:
  - `accept()`: Async method returning `(UnixStream, SocketAddr)`
  - `poll_accept()`: Non-async version for manual future implementation

### 3. OS-Specific Handling
- Special cases for Linux/Android abstract sockets
- File descriptor management using Unix-specific traits (`AsRawFd`, `IntoRawFd`)
- Conditional compilation for platform-specific features

### 4. Integration with Tokio Runtime
- Uses `PollEvented` to interface with Tokio's reactor
- Implements proper task wakeup through `Interest::READABLE` notifications
- Maintains cancel safety for async operations

## Relationship to Project
Part of Tokio's networking stack, this implementation:
- Complements TCP/UDP implementations with Unix domain socket support
- Follows similar patterns to `TcpListener` for API consistency
- Integrates with Tokio's async I/O system through mio integration
- Enables efficient IPC in server applications using Tokio's runtime

## Important Implementation Details
- Abstract socket support via Linux/Android-specific extensions
- File descriptor safety through RAII patterns
- Conversion traits for interoperability with stdlib types
- Error handling propagation through io::Result patterns
- Documentation examples showing async/await usage
