# Tokio I/O Utilities Module (`util/mod.rs`)

## Purpose
This module provides a comprehensive set of utilities for asynchronous I/O operations in Tokio. It extends core async I/O traits with convenience methods, implements buffered I/O adapters, and offers utility functions for common I/O patterns.

## Key Components

### Extension Traits
- **`AsyncBufReadExt`/`AsyncReadExt`/`AsyncSeekExt`/`AsyncWriteExt`**: Add async methods to respective traits (`AsyncBufRead`, `AsyncRead`, etc.) through blanket implementations.
- **Example Methods**: `read_exact()`, `write_all()`, `flush()`, `seek()`

### Buffered I/O Types
- **`BufReader`/`BufWriter`**: Add buffering to async readers/writers (8KB default buffer)
- **`BufStream`**: Bidirectional buffering for full-duplex streams

### Core Utilities
- **Data Copy Functions**:
  - `copy()`: Basic async copy between reader and writer
  - `copy_buf()`: Optimized version using buffered reading
  - `copy_bidirectional()`: Full-duplex copying between two streams
- **Special Streams**:
  - `Empty`: Infinite reader producing no data
  - `Repeat`: Infinite reader repeating given bytes
  - `Sink`: Writer that discards all input

### Protocol Helpers
- `Lines`: Async line reader implementation
- `read_int`/`write_int`: Primitive type serialization helpers
- `read_line`/`read_until`: Pattern-based reading

### Platform Integration
- `DuplexStream`/`SimplexStream`: Memory-backed async streams
- Process I/O support through `read_to_end` (used with `cfg_process!`)

### Concurrency Control
- `poll_proceed_and_make_progress()`: Cooperative scheduling integration that:
  - Checks task budget with `coop::poll_proceed`
  - Marks progress when using cooperative mode

## Conditional Compilation
- **`cfg_io_util!`**: Main implementation gated behind I/O utility feature
- **`cfg_process!`**: Process-specific utilities like `read_to_end`
- **`cfg_coop!`**: Cooperative scheduling integration

## Project Integration
- Serves as the foundation for Tokio's async I/O ecosystem
- Implements patterns from `std::io` in async context
- Used by higher-level components like TCP/UDP networking and file I/O
- Provides building blocks for protocol implementations and stream processing
