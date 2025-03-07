# BufStream in Tokio's I/O Utilities

## Purpose
The `BufStream` struct provides bidirectional buffering for types implementing both `AsyncRead` and `AsyncWrite`. It combines `BufReader` and `BufWriter` to minimize syscall overhead for both read and write operations in asynchronous I/O.

## Key Components

### Struct Definition
- **`BufStream<RW>`**: Wraps an inner `BufReader<BufWriter<RW>>` to buffer both directions:
  - `BufWriter` buffers outgoing data.
  - `BufReader` buffers incoming data.

### Core Functionality
- **Construction**:
  - `new(stream: RW)`: Creates a default-sized buffered stream.
  - `with_capacity()`: Allows specifying buffer sizes for reader/writer.
- **Accessors**:
  - `get_ref()`, `get_mut()`, `get_pin_mut()`: Access the underlying I/O object.
  - `into_inner()`: Extracts the inner stream (discarding buffered data).
- **Trait Implementations**:
  - `AsyncRead`, `AsyncWrite`, `AsyncSeek`, `AsyncBufRead`: Delegated to the inner buffered reader/writer.
  - `From` conversions: Handles inversion of `BufReader`/`BufWriter` nesting.

### Special Handling
- **Seeking**: Discards internal buffers during seeks to maintain positional consistency with the underlying stream.
- **Bidirectional Buffering**: Ensures efficient I/O by reducing syscalls for both reads and writes.

## Integration with the Project
- Part of Tokio's `io-util` module, enhancing performance for bidirectional streams.
- Complements other utilities like `BufReader`, `BufWriter`, and async adapters.
- Used in scenarios requiring efficient buffered I/O (e.g., network protocols, file operations).

---
