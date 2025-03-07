# poll_buf.rs Explanation

## Purpose
This file provides two core utility functions (`poll_read_buf` and `poll_write_buf`) that bridge Tokio's asynchronous I/O operations with the `bytes` crate's buffer types. It enables efficient zero-copy handling of I/O operations using async/await patterns.

## Key Components

### 1. poll_read_buf
- **Function**: Reads data from an `AsyncRead` source into a `BufMut` buffer
- **Key Features**:
  - Handles uninitialized memory safely using `ReadBuf`
  - Automatically advances buffer position after read
  - Returns `Poll<Result<usize>>` for async integration
- **Safety**: Uses `unsafe` to work with uninitialized memory through `MaybeUninit`

### 2. poll_write_buf
- **Function**: Writes data from a `Buf` buffer to an `AsyncWrite` destination
- **Key Features**:
  - Supports vectored I/O when available
  - Handles up to 64 I/O slices (MAX_BUFS)
  - Automatically advances buffer cursor after write
  - Falls back to regular write if vectored writes unsupported

## Integration with Project
- Works with Tokio's async I/O primitives (`AsyncRead`, `AsyncWrite`)
- Integrates with `bytes` crate's buffer types (`Buf`, `BufMut`)
- Used by higher-level components like `StreamReader` for stream-to-IO conversion
- Enables efficient buffer management in async contexts

## Examples
- Reading from a `StreamReader` into `BytesMut`
- Writing from a `Cursor<&[u8]>` to a `File`
- Demonstrates proper usage of async polling with `poll_fn`

## Safety Considerations
- Proper use of `ReadBuf` ensures safe handling of uninitialized memory
- Pointer validation after read operations
- Buffer advancement guarded by actual bytes read/written

This file provides foundational buffer I/O operations for Tokio's async ecosystem, enabling efficient data transfer between I/O sources and byte buffers while maintaining async semantics.
