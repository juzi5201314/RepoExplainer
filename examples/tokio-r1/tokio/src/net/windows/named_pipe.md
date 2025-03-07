# Windows Named Pipe Implementation in Tokio

## Purpose
This module provides asynchronous support for Windows named pipes, enabling inter-process communication (IPC) between server and client applications. It integrates with Tokio's runtime to offer non-blocking I/O operations, allowing efficient handling of pipe connections and data transfer.

## Key Components

### 1. **NamedPipeServer**
- **Role**: Represents the server end of a named pipe.
- **Key Methods**:
  - `connect()`: Asynchronously waits for client connections.
  - `disconnect()`: Terminates the current connection.
  - Async I/O methods (`readable()`, `writable()`, `try_read()`, `try_write()`).
- **Integration**: Implements `AsyncRead` and `AsyncWrite` for seamless use with Tokio's I/O utilities.

### 2. **NamedPipeClient**
- **Role**: Represents the client end of a named pipe.
- **Key Methods**: Similar async I/O methods as the server.
- **Connection Handling**: Retries on busy pipes (e.g., `ERROR_PIPE_BUSY`).

### 3. **ServerOptions & ClientOptions**
- **Builder Patterns**: Configure pipe properties before creation.
  - **ServerOptions**: Sets pipe mode (byte/message), access direction (inbound/outbound), security settings, and instance limits.
  - **ClientOptions**: Configures read/write permissions and security flags.
- **Windows API Integration**: Uses `CreateNamedPipeW` (server) and `CreateFileW` (client).

### 4. **Pipe Configuration**
- **PipeMode**: `Byte` (stream-like) or `Message` (packet-like).
- **PipeEnd**: Identifies server/client ends.
- **PipeInfo**: Metadata about a pipe (mode, buffer sizes, etc.).

### 5. **Async Readiness Handling**
- Uses `PollEvented` from Tokio to interface with `mio` for event polling.
- Methods like `ready()` and `async_io()` manage I/O readiness notifications.

## Integration with Tokio
- **Runtime Dependency**: Requires Tokio runtime with I/O enabled.
- **Async Traits**: Implements `AsyncRead`/`AsyncWrite` for interoperability with Tokio's ecosystem.
- **Cancellation Safety**: Methods like `connect()` support safe cancellation.

## Example Workflow
1. **Server Setup**:
   ```rust
   let server = ServerOptions::new().create(r"\\.\pipe\example")?;
   server.connect().await?;
   ```
2. **Client Connection**:
   ```rust
   let client = ClientOptions::new().open(r"\\.\pipe\example")?;
   ```
3. **Data Transfer**:
   - Use `try_read()`/`try_write()` with readiness polling.

## Error Handling
- Handles Windows-specific errors (e.g., `ERROR_PIPE_BUSY`) with retry logic.
- Converts OS errors to Rust's `io::Error` types.

## Role in the Project