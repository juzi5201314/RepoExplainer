# Tokio-Stream `LinesStream` Wrapper

## Purpose
This file provides a `LinesStream` type that wraps Tokio's `tokio::io::Lines` to implement the `Stream` trait. It enables asynchronous line-by-line processing of buffered input (e.g., files, network streams) using Tokio's stream utilities.

## Key Components

### Struct Definition
- **`LinesStream<R>`**: Wraps a pinned `tokio::io::Lines<R>` where `R: AsyncBufRead`.
  - Implements `Stream` to produce `io::Result<String>` items (lines from input).
  - Maintains compatibility with original `Lines` through accessors like `into_inner()`.

### Core Functionality
1. **Stream Implementation**:
   - `poll_next()` delegates to `Lines::poll_next_line()`, converting the result to a `Stream`-compatible output using `Result::transpose`.
   - Enables async iteration via `StreamExt` (e.g., `stream.next().await`).

2. **Interoperability**:
   - `AsRef`/`AsMut` implementations expose the inner `Lines` type.
   - `as_pin_mut()` allows direct access to the pinned inner `Lines` for advanced use cases.

### Example Usage
Shows how to read lines from a byte buffer as a stream:
```rust
let input = b"Hello\nWorld\n";
let mut stream = LinesStream::new(input.lines());
while let Some(line) = stream.next().await { /* ... */ }
```

## Project Context
- Part of Tokio's `tokio-stream` crate, which provides stream utilities.
- Bridges Tokio's I/O primitives (`AsyncBufRead`) with the `Stream` ecosystem.
- Similar to other wrappers (e.g., for `Split` or `Receiver`), ensuring consistent async processing patterns.

---
