# BytesCodec Explanation

## Purpose
The `BytesCodec` provides a minimalistic implementation of Tokio's `Decoder` and `Encoder` traits for handling raw byte streams without additional framing. It enables direct conversion between I/O resources (like TCP streams) and byte chunks (`BytesMut`), making it suitable for scenarios requiring unprocessed byte handling.

## Key Components

### Struct Definition
```rust
pub struct BytesCodec(());
```
- A zero-sized type (unit struct with empty tuple) for efficiency.
- Implements `Copy`, `Clone`, and other basic traits.

### Core Implementations
1. **Decoder**:
   ```rust
   fn decode(&mut self, buf: &mut BytesMut) -> Result<Option<BytesMut>, io::Error> {
       if !buf.is_empty() {
           let len = buf.len();
           Ok(Some(buf.split_to(len)))
       } else {
           Ok(None)
       }
   }
   ```
   - Consumes all available bytes from the input buffer in one operation
   - Returns `BytesMut` containing the full buffer contents when data exists

2. **Encoder** (for both `Bytes` and `BytesMut`):
   ```rust
   fn encode(&mut self, data: T, buf: &mut BytesMut) -> Result<(), io::Error> {
       buf.reserve(data.len());
       buf.put(data);
       Ok(())
   }
   ```
   - Appends incoming bytes directly to the output buffer
   - Handles both `Bytes` and `BytesMut` input types

## Usage Example
```rust
let my_async_read = File::open("filename.txt").await?;
let my_stream_of_bytes = FramedRead::new(my_async_read, BytesCodec::new());
```
- Converts an `AsyncRead` into a stream of `Result<BytesMut, io::Error>`
- Suitable for scenarios requiring direct byte access without protocol parsing

## Project Context
- Part of Tokio's codec utilities (`tokio_util::codec`)
- Serves as base infrastructure for:
  - Building more complex codecs (e.g., length-prefixed or delimiter-based)
  - Raw byte streaming in network protocols
  - Bridging I/O resources with byte processing pipelines
- Complements other codecs like `LengthDelimitedCodec` by providing zero-overhead raw byte handling
