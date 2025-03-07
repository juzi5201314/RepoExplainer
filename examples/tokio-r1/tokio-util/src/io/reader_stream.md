# ReaderStream in tokio-util

## Purpose
The `ReaderStream` struct converts an [`AsyncRead`](https://docs.rs/tokio/latest/tokio/io/trait.AsyncRead.html) source into a [`Stream`](https://docs.rs/futures-core/latest/futures_core/stream/trait.Stream.html) of byte chunks (`Result<Bytes, std::io::Error>`). It enables incremental processing of asynchronous I/O data via stream semantics, performing the inverse operation of [`StreamReader`](https://docs.rs/tokio-util/latest/tokio_util/io/struct.StreamReader.html).

## Key Components
1. **Struct Fields**:
   - `reader: Option<R>`: The wrapped `AsyncRead` source (set to `None` on termination/error).
   - `buf: BytesMut`: Reusable buffer for reading data.
   - `capacity: usize`: Initial buffer capacity (default: 4096).

2. **Constructors**:
   - `new(reader: R)`: Creates a stream with default buffer capacity.
   - `with_capacity(reader: R, capacity: usize)`: Allows custom initial buffer size.

3. **Stream Implementation**:
   - Uses `poll_read_buf` to asynchronously read into `BytesMut`.
   - Splits filled buffer chunks into immutable `Bytes` for stream emission.
   - Handles termination on EOF (`Ok(0)`) or errors by setting `reader` to `None`.

## Example Usage
```rust
let data = b"hello";
let mut stream = ReaderStream::new(&data[..]);
while let Some(chunk) = stream.next().await {
    // Process chunk
}
```

## Integration with Project
- Part of Tokio's utility ecosystem (`tokio-util`), bridging async I/O and stream processing.
- Complements `StreamReader` (converts `Stream` to `AsyncRead`).
- Used in scenarios requiring stream-based consumption of I/O sources (e.g., network/file data).

---
