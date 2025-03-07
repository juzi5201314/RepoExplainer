# Code File Explanation: `framed.rs`

## Purpose
The `framed.rs` file defines the `Framed` struct, which provides a unified [`Stream`] and [`Sink` interface for asynchronous I/O operations. It bridges raw byte streams (like TCP connections) and structured data frames using customizable `Encoder` and `Decoder` traits. This allows developers to work with high-level message frames instead of low-level byte manipulation.

## Key Components

### 1. **`Framed` Struct**
- **Role**: Combines an I/O object (e.g., a TCP stream) with a codec to handle frame encoding/decoding.
- **Fields**:
  - `inner: FramedImpl`: Delegates core logic to an internal implementation (`FramedImpl`).
- **Key Methods**:
  - `new()`: Creates a `Framed` instance with default buffers.
  - `with_capacity()`: Initializes with a specified read buffer capacity.
  - `from_parts()`: Reconstructs a `Framed` from components (I/O, codec, buffers).
  - Buffer accessors (`read_buffer()`, `write_buffer_mut()`, etc.): Allow direct buffer manipulation.
  - Codec utilities (`codec()`, `map_codec()`): Access or transform the codec.

### 2. **`FramedParts` Struct**
- **Role**: Holds decomposed parts of a `Framed` instance (I/O object, codec, read/write buffers). Used to rebuild or modify `Framed` instances.
- **Fields**: `io`, `codec`, `read_buf`, `write_buf`.

### 3. **Trait Implementations**
- **`Stream`**: Delegates to `FramedImpl` to poll for decoded frames using the `Decoder`.
- **`Sink<I>`**: Delegates to `FramedImpl` to encode and write items using the `Encoder`.

### 4. **Buffer Management**
- Read/write buffers (`BytesMut`) store raw bytes during decoding/encoding.
- Methods like `read_buffer_mut()` expose buffers for advanced use cases.

## Integration with the Project
- **Codec System**: Integrates with `Encoder` and `Decoder` traits (from `tokio_util::codec`) to handle frame serialization/deserialization.
- **Async I/O**: Works with Tokio's `AsyncRead` and `AsyncWrite` traits, enabling compatibility with Tokio's runtime and networking primitives.
- **Utilities**: Used in higher-level protocols (e.g., HTTP, WebSocket) to manage frame-based communication.

## Example Flow
1. **Reading**: Raw bytes from an I/O source (e.g., socket) are buffered and decoded into frames via `Stream::poll_next`.
2. **Writing**: Frames are encoded into bytes via `Sink::start_send` and flushed to the I/O sink.

## Cancellation Safety
- Ensures safe usage in `tokio::select!` contexts (e.g., dropped sends don't corrupt state).

---
