# Tokio AsyncBufReadExt Utility Module

## Purpose
This file provides extension methods for asynchronous buffered readers through the `AsyncBufReadExt` trait. It adds high-level utility methods to types implementing `AsyncBufRead`, simplifying common I/O operations like reading until a delimiter, splitting streams, and line-by-line processing in async contexts.

## Key Components

### 1. Core Traits
- **`AsyncBufReadExt`**: The main extension trait defining methods for:
  - `read_until`: Read bytes until a delimiter
  - `read_line`: Read a line (UTF-8 validated)
  - `split`: Split stream by delimiter
  - `fill_buf`/`consume`: Low-level buffered I/O control
  - `lines`: Stream of lines

### 2. Method Implementations
Each method returns a future or stream:
- `ReadUntil`: Future for delimiter-based reading
- `ReadLine`: Future for line reading with UTF-8 validation
- `Split`: Stream of byte segments
- `Lines`: Stream of parsed strings
- `FillBuf`: Future for buffer management

### 3. Important Features
- **Cancellation Safety**: Documented behavior for async operation interruption
- **UTF-8 Handling**: Automatic validation in `read_line`
- **Zero-Copy Operations**: Buffer reuse in `read_until` and `fill_buf`
- **Stream Processing**: Iterator-like patterns via `split` and `lines`

## Integration with Project
- Works with Tokio's async I/O primitives (e.g., `TcpStream`, `UnixStream`)
- Complements other IO utilities (`BufReader`, `BufWriter`)
- Used in network protocols and data processing pipelines
- Enables composition with Tokio's async ecosystem through futures and streams

## Relationship to Other Components
- Depends on low-level async traits (`AsyncBufRead`, `AsyncRead`)
- Used by higher-level network types through trait implementation
- Integrates with Tokio's split I/O pattern (`ReadHalf`/`WriteHalf`)

## Key Design Aspects
- **Ergonomics**: Chainable async operations
- **Efficiency**: Minimizes allocations through buffer reuse
- **Safety**: Clear documentation of cancellation behavior
- **Extensibility**: Blanket implementation for all `AsyncBufRead` types
