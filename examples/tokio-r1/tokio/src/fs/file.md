# Tokio File Module Explanation

## Purpose
This module provides asynchronous file I/O operations for the Tokio runtime by wrapping synchronous `std::fs::File` operations and executing them in a blocking thread pool. It implements `AsyncRead`, `AsyncWrite`, and `AsyncSeek` traits to enable non-blocking file interactions.

## Key Components

### 1. File Struct
- **Wraps**: 
  - `Arc<StdFile>`: Thread-safe reference to the standard file handle
  - `Mutex<Inner>`: Synchronizes access to file state and buffers
  - `max_buf_size`: Configurable buffer size for I/O operations
- **State Management**:
  - `Inner` struct tracks:
    - `state`: Current operation state (Idle/Busy)
    - `last_write_err`: Captures write errors detected during read operations
    - `pos`: Logical cursor position

### 2. Async Operations
- **Non-blocking Execution**:
  - Uses `spawn_blocking` to run file operations in a dedicated thread pool
  - Implements future-based async patterns via `poll_read`/`poll_write`
- **Buffering**:
  - `Buf` structure manages data transfer between async and sync contexts
  - Implements copy optimizations with `copy_to` (read) and `copy_from` (write)

### 3. Core Functionality
- **File Operations**:
  - `open()`, `create()`, `sync_all()`, `set_len()`, `metadata()`
  - Implements atomic create-new with `create_new()`
- **Conversion**:
  - `from_std()`/`into_std()` for interoperability with synchronous code
  - `try_clone()` for shared file handle access

### 4. Error Handling
- Tracks write errors during read operations via `last_write_err`
- Propagates OS errors through async error channels

### 5. Platform Integration
- Implements OS-specific traits (`AsRawFd` for Unix, `AsRawHandle` for Windows)
- Uses conditional compilation for platform-specific logic

## Integration with Project
- **Runtime Integration**: Leverages Tokio's blocking thread pool via `spawn_blocking`
- **IO Traits**: Implements core async traits (`AsyncRead`, `AsyncWrite`, `AsyncSeek`) for seamless integration with Tokio's IO ecosystem
- **Testing**: Uses mocked file operations (`MockFile`) and thread pool during tests

## Example Flow (Async Read)
1. Call `file.read_to_end()` 
2. Check if buffer has data -> return immediately
3. If no data, spawn blocking task to read from `StdFile`
4. Yield until blocking task completes
5. Copy data from internal buffer to user buffer
6. Update cursor position
