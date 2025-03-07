# LinesCodec Explanation

## Purpose
The `LinesCodec` provides line-based encoding/decoding functionality for Tokio's asynchronous I/O operations. It splits byte streams into lines (using `\n` as delimiter) and ensures safe handling of input data with configurable maximum line lengths to prevent memory exhaustion attacks.

## Key Components

### Struct Fields
- `next_index`: Optimizes line searching by tracking position between decode calls
- `max_length`: Security measure to limit maximum line length (default: unlimited)
- `is_discarding`: State flag for handling over-length lines

### Core Functionality
1. **Decoding**:
   - Efficiently finds newline characters using remembered `next_index`
   - Handles carriage returns (`\r\n` Windows-style endings)
   - Enforces maximum line length with `LinesCodecError::MaxLineLengthExceeded`
   - Implements streaming-aware EOF handling

2. **Encoding**:
   - Appends `\n` to outgoing strings
   - Efficient buffer management with `BytesMut`

### Error Handling
- `LinesCodecError` enum with variants for:
  - Line length violations
  - I/O errors (including UTF-8 decoding failures)
- Automatic conversion from `io::Error`

### Security Features
- Configurable `max_length` prevents unbounded memory consumption
- Safe discard mechanism for over-length lines
- UTF-8 validation during decoding

## Integration with Project
This codec integrates with Tokio's codec system through:
- `Decoder` trait implementation for parsing incoming bytes
- `Encoder` trait implementation for formatting outgoing messages
- Designed to work with `tokio_util::codec::Framed` for stream processing

## Usage Patterns
Typical use cases include:
- Network protocols like SMTP or HTTP headers
- Log processing pipelines
- Chat applications using line-based messaging
- Any text-based protocol requiring line segmentation

## Optimization Aspects
- State preservation between decode calls (`next_index`)
- Minimal buffer copying through `BytesMut` operations
- Early-return patterns to avoid unnecessary processing
