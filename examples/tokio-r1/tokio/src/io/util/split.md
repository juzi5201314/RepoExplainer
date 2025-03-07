# Code Explanation: `tokio/src/io/util/split.rs`

## Purpose
This file implements the `Split` utility for asynchronously splitting an `AsyncBufRead` stream into byte segments based on a delimiter. It enables efficient, non-blocking processing of delimited data (e.g., splitting a byte stream by newlines or custom separators).

## Key Components

### 1. `Split` Struct
- **Definition**: A pinned struct containing:
  - `reader`: The underlying `AsyncBufRead` input source.
  - `buf`: A buffer to accumulate bytes until the delimiter is found.
  - `delim`: The delimiter byte (e.g., `b'\n'`).
  - `read`: Tracks progress during partial reads.
- **Role**: Manages state for splitting the input stream into segments.

### 2. `split` Constructor
- Initializes a `Split` instance with an empty buffer and the specified delimiter.

### 3. Async Methods
- `next_segment`: 
  - An async method that returns the next segment as `Option<Vec<u8>>`.
  - Internally wraps `poll_next_segment` into an async-friendly interface using `poll_fn`.
- `poll_next_segment`:
  - Core polling method that uses `read_until_internal` to read until the delimiter.
  - Handles buffer management, delimiter removal, and end-of-stream detection.

### 4. Integration with Tokio
- Works with `AsyncBufReadExt::split` to provide a stream-like API.
- Designed to be wrapped into a `Stream` via `SplitStream` (from `tokio-stream`).

## How It Fits Into the Project
- Part of Tokio's I/O utilities (`io-util` feature).
- Complements other async I/O primitives like `read_until` and `Lines`.
- Enables use cases like parsing protocols or chunked data without blocking.

## Example Flow
1. A user calls `my_reader.split(b';')` to create a `Split` instance.
2. Repeatedly calls `next_segment().await` to get byte segments separated by `;`.
3. Internally, `poll_next_segment` reads data incrementally, splits on `;`, and returns each segment.

---
