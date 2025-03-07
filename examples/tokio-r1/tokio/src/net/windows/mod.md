# Windows Network Types Module (`mod.rs`)

## Purpose
This module provides Windows-specific implementations for named pipe communication in Tokio, enabling asynchronous inter-process communication (IPC) through Windows named pipes.

## Key Components
1. **Named Pipe Types**:
   - `NamedPipeClient`: Represents a client-side connection to a named pipe
   - `NamedPipeServer`: Represents a server-side listener for pipe connections

2. **Builder Patterns**:
   - `ServerOptions`: Configures and creates pipe servers with methods like `create()`
   - `ClientOptions`: Configures and opens pipe client connections with methods like `open()`

3. **Integration**:
   - Wraps low-level `mio_windows::NamedPipe` with `PollEvented` for async I/O integration
   - Handles Windows-specific error codes (e.g., `ERROR_PIPE_BUSY`, `ERROR_PIPE_NOT_CONNECTED`)

4. **Features**:
   - Pipe mode configuration (message/byte streams)
   - Security attributes handling
   - Remote client acceptance/rejection controls
   - Pipe metadata retrieval

## Project Context
- Part of Tokio's platform-specific networking implementation
- Complements Unix domain socket functionality but for Windows IPC
- Provides async/await compatible interface over Windows named pipe API
- Integrates with Tokio's reactor system through `mio` event polling

## Usage Patterns
```rust
// Server setup
let server = ServerOptions::new()
    .reject_remote_clients(true)
    .create(PIPE_NAME)?;

// Client connection
let client = ClientOptions::new()
    .open(PIPE_NAME)?;
```

## Implementation Details
- Uses Windows API constants (e.g., `PIPE_REJECT_REMOTE_CLIENTS`)
- Handles pipe creation flags and attributes
- Implements proper error conversion from Windows error codes
- Provides documentation examples for common use cases and error handling
