# BufReader in Tokio's I/O Utilities

## Purpose
The `BufReader` struct provides buffered asynchronous reading by wrapping an underlying `AsyncRead` implementation. It optimizes small, frequent read operations by maintaining an in-memory buffer, reducing direct interactions with the async reader. This is particularly useful for network streams or file I/O where system call overhead is significant.

## Key Components

### Struct Definition
- **Fields**:
  - `inner`: The wrapped async reader (e.g., TCP stream, file).
  - `buf`: A fixed-size buffer (default 8KB) for storing pre-fetched data.
  - `pos`/`cap`: Track the current read position and total buffered data length.
  - `seek_state`: Manages state during seek operations (`SeekState` enum).

### Core Functionality
1. **Buffered Reading**:
   - Implements `AsyncRead` and `AsyncBufRead` to serve data from the buffer.
   - `poll_fill_buf`: Refills the buffer when empty by reading from `inner`.
   - `consume`: Advances the buffer position after data is read.

2. **Large Read Optimization**:
   - Bypasses the buffer for reads larger than the buffer size to avoid double buffering.

3. **Seeking Support**:
   - Implements `AsyncSeek` with careful handling of buffer invalidation during seeks.
   - Uses `SeekState` to track multi-step seek operations (e.g., overflow handling).

4. **Passthrough Writing**:
   - Delegates `AsyncWrite` methods directly to the underlying `inner` writer if supported.

### Methods
- **Construction**: `new()` and `with_capacity()` initialize the buffer.
- **Accessors**: `get_ref()`, `get_mut()`, `buffer()` for introspection.
- **Buffer Management**: `discard_buffer()` clears buffered data (used during seeks).

## Integration with Tokio
- Part of Tokio's `io-util` module, designed to work with async I/O traits (`AsyncRead`, `AsyncWrite`, `AsyncSeek`).
- Complements other utilities like `BufWriter` and interacts with async streams/sockets.
- Handles edge cases in async contexts (e.g., partial reads, seek consistency).

## Example Flow
1. **Read Request**:
   - Check if buffer has data. If yes, serve from buffer.
   - If buffer is empty, fetch data into buffer via `poll_fill_buf`.
   - Copy data to user buffer and update `pos`.

2. **Seek Operation**:
   - Invalidate buffer to ensure position consistency.
   - Delegate seek to `inner` reader while tracking state transitions.

---
