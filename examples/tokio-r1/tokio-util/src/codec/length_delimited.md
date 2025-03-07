# Tokio-util Length-Delimited Codec Explanation

## Purpose
The `length_delimited.rs` file implements a codec for framing byte streams using length prefixes. It handles both encoding and decoding of messages where each frame is prefixed with its length, enabling protocol implementations to work with complete frames without manual buffering or fragmentation logic.

## Key Components

### 1. Core Structures
- **`LengthDelimitedCodec`**: Main codec type implementing `Decoder` and `Encoder` traits.
  - Decodes byte streams into `BytesMut` frames.
  - Encodes `Bytes` payloads with length headers.
- **`Builder`**: Configures codec parameters using fluent interface pattern.
  - Allows customization of length field position/size, endianness, max frame size, and header adjustments.

### 2. Configuration Parameters
- **Length Field**: Position (offset), size (1-8 bytes), and endianness (big/little/native)
- **Adjustments**: Mathematical adjustments to header values
- **Skipping**: Bytes to skip before payload
- **Max Frame Length**: Security limit (default 8MB)

### 3. Decoding Process
1. Read length header based on configured position/endianness
2. Apply length adjustments (positive/negative offsets)
3. Verify against max frame length
4. Extract payload while handling partial reads

### 4. Encoding Process
1. Validate payload length against max frame size
2. Calculate adjusted length value
3. Write header with proper endianness
4. Append payload data

## Protocol Flexibility
Supports diverse protocol requirements through configuration:
- Variable header positions (e.g., length after version bytes)
- Composite headers (length + metadata)
- Length representations including/excluding header size
- Big/Little Endian compatibility

## Integration with Tokio
- Works with `Framed`, `FramedRead`, and `FramedWrite` for async I/O integration
- Implements Tokio's codec traits for seamless use with async streams/sinks

## Error Handling
- **`LengthDelimitedCodecError`**: Specialized error for frame size violations
- Overflow protection for length calculations
- IO error propagation for underlying stream failures

## Example Use Case
```rust
// Create codec with 2-byte little-endian length header
let codec = LengthDelimitedCodec::builder()
    .length_field_type::<u16>()
    .little_endian()
    .new_codec();

// Adapt async I/O stream
let framed = Framed::new(socket, codec);
```

## Project Role
Provides fundamental length-prefixed message framing for Tokio-based network protocols, abstracting low-level byte stream handling while offering extensive configuration options for protocol-specific requirements.
