# Code Explanation: `read_until.rs`

## Purpose
This file implements an asynchronous utility for reading bytes from a buffered I/O source until a specified delimiter is encountered. The delimiter is included in the result, and the implementation is designed to work efficiently within Tokio's async runtime.

## Key Components

### `ReadUntil` Struct
- **Future Type**: Represents the asynchronous operation of reading until the delimiter is found.
- **Fields**:
  - `reader`: A mutable reference to the buffered reader (`AsyncBufRead`).
  - `delimiter`: The byte to search for.
  - `buf`: A mutable reference to the output buffer (stores data including the delimiter).
  - `read`: Tracks the number of bytes appended during this operation.
  - `_pin`: Ensures the future is `!Unpin` for async trait compatibility.

### `read_until` Constructor
- Creates a `ReadUntil` future, initializing the reader, delimiter, buffer, and internal state.

### `read_until_internal` Function
- **Core Logic**: Polls the reader, searches for the delimiter using `memchr`, and appends data to the buffer.
  - If the delimiter is found, the buffer includes all bytes up to and including the delimiter.
  - If not found, continues reading until no more data is available.
- Returns `Poll::Ready` when the delimiter is found or the stream ends.

### `Future` Implementation
- The `poll` method delegates to `read_until_internal`, advancing the reader and updating the buffer asynchronously.

## Integration with the Project
- Part of Tokio's I/O utilities, specifically for `AsyncBufReadExt::read_until`.
- Composes with other async I/O primitives (e.g., `AsyncRead`, `AsyncSeek`) to enable non-blocking operations.
- Uses `pin_project!` to safely handle pinning, a common pattern in Tokio for async futures.

## Key Design Choices
- **Efficiency**: Uses `memchr` for fast byte scanning and minimizes buffer reallocations.
- **Async Safety**: Ensures proper pinning and state management for compatibility with async/await syntax.
- **Inclusion of Delimiter**: Matches the behavior of `std::io::BufRead::read_until`, ensuring consistency with synchronous APIs.

---
