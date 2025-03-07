# UDP Framing Module in Tokio-util

## Purpose
This module provides asynchronous UDP socket handling with message framing capabilities for Tokio applications. It enables structured message processing over UDP by combining raw sockets with encoder/decoder components.

## Key Components

### 1. UdpFramed Struct
- **Core Type**: Combines a UDP socket with codec for message serialization
- **Components**:
  - `socket`: Underlying UDP socket (Tokio or standard)
  - `codec`: Message encoder/decoder implementation
  - Buffers (`rd`, `wr`) for read/write operations
  - Address tracking (`out_addr`) for replies
- **Capabilities**:
  - Implements `Stream` for async message reception
  - Implements `Sink` for async message sending
  - Handles message boundaries and address association

### 2. UdpSocket Implementation
- Tokio-compatible wrapper around `mio::net::UdpSocket`
- Features async I/O integration through `PollEvented`
- Provides conversion methods between Tokio and standard sockets
- Handles non-blocking mode configuration

### 3. Framing Infrastructure
- Leverages `Encoder`/`Decoder` traits for message processing
- Uses separate buffers for incoming/outgoing data
- Manages socket readiness states (`is_readable`, `flushed`)

## Integration Points
- Works with Tokio's async runtime through `Stream`/`Sink` interfaces
- Compatible with any codec implementing the required traits
- Supports cross-platform operation with Unix-specific optimizations
- Integrates with standard library sockets through conversion methods

## Typical Usage
```rust
let socket = UdpSocket::bind(address).await?;
let framed = UdpFramed::new(socket, MyCodec::new());

// Send messages with destination addresses
framed.send((message, dest_addr)).await?;

// Receive decoded messages with source addresses
while let Some(Ok((msg, src_addr))) = framed.next().await {
    // Handle message
}
```

## Role in Project