# StreamReader in tokio-util

## Purpose
The `StreamReader` struct converts a [`Stream`] of byte chunks (e.g., `Bytes` or `Buf`-implementing types) into an [`AsyncRead`] or [`AsyncBufRead`] interface. This enables asynchronous consumption of streamed data via standard I/O methods like `read` or `read_line`, bridging the gap between stream-based and I/O-based processing.

## Key Components

### Struct Definition
```rust
pub struct StreamReader<S, B> {
    inner: S,      // Underlying stream producing byte chunks
    chunk: Option<B>, // Current buffer being read from
}
```
- **`inner`**: The input stream yielding `Result<B, E>` items, where `B: Buf`.
- **`chunk`**: Holds the current byte buffer being read. Empty chunks are automatically skipped.

### Core Functionality
1. **Conversion**:
   - Implements `AsyncRead` and `AsyncBufRead` to allow reading from the stream as a continuous byte sequence.
   - Handles chunk boundaries, buffering, and errors transparently.

2. **Methods**:
   - `new(stream: S)`: Creates a `StreamReader` from a stream.
   - `into_inner_with_chunk()`: Returns the underlying stream and any remaining buffered data.
   - `get_ref()`, `get_mut()`, `get_pin_mut()`: Accessors for the inner stream.

3. **Async Traits**:
   - **`AsyncRead::poll_read`**: Reads bytes into a buffer, fetching new chunks from the stream as needed.
   - **`AsyncBufRead::poll_fill_buf`**: Provides direct access to the current chunk's bytes for efficient line reading.
   - **`consume()`**: Advances the internal buffer position after a read.

### Error Handling
- Stream errors of type `E` are converted to `std::io::Error` using `E: Into<io::Error>`.
- Non-I/O errors in the stream must be mapped to `io::Error` before use (see examples).

### Integration with Sink
If the inner stream `S` implements `Sink`, the `StreamReader` forwards `Sink` methods (e.g., `poll_ready`, `start_send`), enabling bidirectional I/O.

## Usage Examples
1. **Basic Reading**:
   ```rust
   let stream = tokio_stream::iter(vec![Ok(Bytes::from_static(&[0,1,2,3]))]);
   let mut reader = StreamReader::new(stream);
   reader.read_exact(&mut buf).await?;
   ```

2. **Error Mapping**:
   ```rust
   let stream = stream.map(|res| res.map_err(|e| io::Error::new(ErrorKind::Other, e)));
   ```

3. **Line-by-Line Reading**:
   ```rust
   let mut reader = StreamReader::new(stream);
   reader.read_line(&mut line).await?;
   ```

## Project Role
This file provides critical interoperability between Tokio's asynchronous I/O traits (`AsyncRead`/`AsyncBufRead`) and stream-based data sources. It is essential for scenarios like:
- Parsing network protocols from chunked data.
- Converting message-oriented streams (e.g., WebSocket frames) into byte streams.
- Enabling I/O utilities (e.g., `read_line`) to work directly with streams.
