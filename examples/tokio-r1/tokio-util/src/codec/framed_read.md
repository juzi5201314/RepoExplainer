# FramedRead Code Explanation

## Purpose
The `FramedRead` struct in `framed_read.rs` provides a streaming interface to decode raw bytes from an `AsyncRead` source into structured messages using a customizable `Decoder`. It handles buffering, partial reads, and async I/O integration for protocol implementations.

## Key Components

### Core Struct
- **`FramedRead<T, D>`**: Main struct wrapping:
  - An async I/O source (`T: AsyncRead`)
  - A decoding mechanism (`D: Decoder`)
  - Internal state (`ReadFrame`) containing:
    - Byte buffer (`BytesMut`)
    - EOF/readability flags
    - Error tracking

### Primary Functionality
1. **Constructors**:
   - `new()`: Creates with default buffer
   - `with_capacity()`: Pre-allocates buffer space

2. **Accessors**:
   - I/O stream access via `get_ref()`, `get_mut()`, `into_inner()`
   - Decoder interaction via `decoder()`, `decoder_mut()`, `map_decoder()`

3. **Buffer Management**:
   - Direct access to read buffer via `read_buffer()`/`read_buffer_mut()`

4. **Async Behavior**:
   - Implements `Stream` for message-by-message polling
   - Delegates to internal `FramedImpl` for actual decoding logic
   - Optional `Sink` implementation passthrough for underlying I/O

## Implementation Details

### Stream Integration
- `poll_next()`: Core async method driving decoding process:
  - Reads bytes from `AsyncRead`
  - Feeds buffer to `Decoder`
  - Yields decoded items or errors

### Error Handling
- Preserves decoder errors while maintaining stream continuity
- Tracks error state to prevent invalid operations after failures

### Memory Management
- Uses `BytesMut` for efficient buffer reuse
- Allows capacity pre-allocation to reduce allocations

## Project Context
Part of Tokio's codec utilities (`tokio-util`), working with:
- **Decoder Trait**: User-implemented message parsing
- **FramedImpl**: Shared internal implementation with `FramedWrite`
- **Async Ecosystem**: Integrates with Tokio's I/O primitives and futures

## Cancellation Safety
- Stream implementation is cancel-safe via reference-based polling
- No message loss when dropping intermediate futures

## Usage Patterns
Typical in protocol implementations:
```rust
let framed = FramedRead::new(tcp_stream, LengthDelimitedDecoder::new());
while let Some(message) = framed.next().await {
    // Handle decoded messages
}
```
