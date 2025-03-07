# Unix Pipe Implementation in Tokio

## Purpose
This file provides asynchronous Unix pipe functionality for Tokio, supporting both anonymous pipes and named FIFO files. It enables non-blocking I/O operations integrated with Tokio's event loop.

## Key Components

### 1. Pipe Creation
- **`pipe()`**: Creates anonymous pipes returning `(Sender, Receiver)` tuple
- Uses `mio_pipe` internally with Tokio's `PollEvented` for event loop integration

### 2. OpenOptions
- Configures FIFO file opening with Linux-specific features:
  - `read_write()`: Enables read-write mode (Linux-specific)
  - `unchecked()`: Skips FIFO type verification
- Methods:
  - `open_receiver()`: Creates reading end from FIFO
  - `open_sender()`: Creates writing end from FIFO

### 3. Sender/Receiver Types
- **`Sender`** (writing end):
  - Implements `AsyncWrite` with methods like `try_write()`, `writable().await`
  - Conversion to/from blocking/non-blocking file descriptors
- **`Receiver`** (reading end):
  - Implements `AsyncRead` with methods like `try_read()`, `readable().await`
  - Buffer management with vectored I/O support

### 4. Core Functionality
- Non-blocking I/O integration using `Interest` and `Ready` states
- File descriptor validation (`is_pipe()`)
- Mode management:
  - `set_nonblocking()` for async operations
  - `set_blocking()` for conversions

## Integration with Project
- Part of Tokio's Unix networking stack
- Works with Tokio runtime for async task scheduling
- Complementary to other Unix I/O types (`UnixStream`, `UnixDatagram`)
- Used in process communication and inter-task messaging

## Key Features
- Atomic writes for small buffers (<= PIPE_BUF)
- Linux-specific read-write mode support
- Error handling for common pipe scenarios (ENXIO, UnexpectedEof)
- Conversion between async and blocking modes

## Example Usage
```rust
// Create anonymous pipe
let (tx, rx) = pipe::pipe()?;

// Named pipe with OpenOptions
let rx = OpenOptions::new().open_receiver("fifo_file")?;
let tx = OpenOptions::new().open_sender("fifo_file")?;

// Async write/read operations
tx.writable().await?.try_write(b"data");
rx.readable().await?.try_read(&mut buffer);
```
