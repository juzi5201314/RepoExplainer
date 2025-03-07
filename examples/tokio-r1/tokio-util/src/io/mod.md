# IO Utilities Module (`tokio-util/src/io/mod.rs`)

## Purpose
This module provides utilities for bridging asynchronous I/O operations with synchronous code, converting between stream/sink abstractions and async I/O traits, and offering debugging/inspection tools. It serves as an extension to Tokio's core I/O primitives, enabling interoperability with libraries like `hyper` and `reqwest`.

## Key Components

### Core Adapters
- **`ReaderStream`/`StreamReader`**: Convert between `AsyncRead` and `Stream<Item = Result<Bytes>>`.
- **`SinkWriter`**: Adapts a `Sink` to an `AsyncWrite` for integration with byte-oriented I/O.
- **`SyncIoBridge`**: Bridges async I/O (e.g., `AsyncRead`, `AsyncWrite`) to synchronous I/O traits (`Read`, `Write`), useful for blocking operations in `spawn_blocking`.

### Utilities
- **`CopyToBytes`**: Efficiently copies data from an `AsyncRead` to a `Bytes` buffer.
- **`InspectReader`/`InspectWriter`**: Wrappers to inspect data during read/write operations (e.g., logging, validation).
- **`read_buf`**: Helper for reading into a `ReadBuf` with async compatibility.
- **`read_exact_arc`**: Reads exact bytes into an `Arc<[u8]>` for shared ownership.

### Compatibility
- **`poll_read_buf`/`poll_write_buf`**: Re-exported utilities for polling read/write operations on buffers.
- **Futures Interop**: Implements `futures_io` traits (e.g., `AsyncSeek`) for Tokio types, ensuring compatibility with `futures`-based code.

## Integration with Project
- **Hyper/Reqwest Integration**: Enables conversion between `hyper::Body` and Tokio's `AsyncRead`, critical for HTTP message handling.
- **Blocking Operations**: `SyncIoBridge` allows synchronous I/O in async contexts via `spawn_blocking`.
- **Stream Processing**: Facilitates use of Tokio I/O primitives in stream/sink pipelines (e.g., gRPC, WebSocket).

## Example Use Cases
- Converting an async TCP stream into a `Stream<Item = Result<Bytes>>` for HTTP parsing.
- Wrapping a synchronous file I/O library in async code using `SyncIoBridge`.
- Debugging data flow in a proxy service with `InspectReader`.

---
