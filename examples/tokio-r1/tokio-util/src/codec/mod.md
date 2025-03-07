# Tokio-Util Codec Module Explanation

## Purpose
This module provides adapters to convert raw byte-oriented I/O (`AsyncRead`/`AsyncWrite`) into structured frame-based streams and sinks (`Stream`/`Sink`). It handles message framing - the process of batching bytes into meaningful protocol units - which is essential for network protocol implementations.

## Key Components

### Core Traits
1. **`Decoder`**
   - Converts incoming bytes into frames
   - Key method: `decode()` handles partial data detection and frame extraction
   - Must handle buffer management and frame validation

2. **`Encoder`**
   - Converts application-level items into byte sequences
   - Key method: `encode()` writes framed data to output buffers
   - Handles message serialization and buffer management

### Main Adapters
1. **`FramedRead`**
   - Adapts `AsyncRead` into a `Stream` of decoded items
   - Uses a `Decoder` implementation to parse frames

2. **`FramedWrite`**
   - Adapts `AsyncWrite` into a `Sink` for encoded items
   - Uses an `Encoder` implementation to serialize frames

3. **`Framed`**
   - Full-duplex adapter combining both reading and writing
   - Implements `Stream + Sink` for bidirectional communication

### Built-in Codecs
1. **`BytesCodec`**
   - Basic codec for raw byte chunks
   - Useful for simple protocols or testing

2. **`LinesCodec`**
   - Newline-delimited text protocol
   - Handles encoding/decoding of string messages

3. **`LengthDelimitedCodec`**
   - Length-prefixed binary protocol
   - Handles frame size validation and buffer management

## Implementation Details
- Uses `bytes::BytesMut` for efficient buffer management
- Implements proper backpressure through `Stream`/`Sink` traits
- Handles partial reads/writes and frame aggregation
- Provides error handling through `std::io::Error` conventions

## Integration with Tokio
- Bridges Tokio's async I/O primitives with futures' Stream/Sink abstractions
- Enables composition with other Tokio utilities and libraries
- Forms foundation for higher-level protocol implementations (e.g., HTTP, WebSocket)

## Example Use Cases
- Implementing network protocols like Redis or Memcached clients
- Creating message-oriented middleware clients
- Building custom RPC frameworks
- Handling structured logging pipelines
