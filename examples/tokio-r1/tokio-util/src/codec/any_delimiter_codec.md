# AnyDelimiterCodec Explanation

## Purpose
This file implements `AnyDelimiterCodec`, a flexible codec for splitting byte streams using multiple delimiter characters. It handles both decoding (splitting input streams into chunks) and encoding (adding delimiters between chunks), with configurable maximum chunk lengths for security.

## Key Components

### 1. Core Struct (`AnyDelimiterCodec`)
- **Fields**:
  - `next_index`: Optimizes delimiter search by tracking progress
  - `max_length`: Security limit for chunk sizes
  - `is_discarding`: Flag for handling oversized chunks
  - `seek_delimiters`: Characters to split on during decoding
  - `sequence_writer`: Delimiter to use during encoding

### 2. Decoder Implementation
- **Key Features**:
  - Efficient scanning using `next_index` position
  - Handles chunk size limits with `max_length`
  - Recovers from oversized chunks via `is_discarding` state
  - Supports partial parsing with `decode_eof`

### 3. Encoder Implementation
- Simple appending of configured `sequence_writer` delimiter
- Works with any string-like input type

### 4. Error Handling
- `AnyDelimiterCodecError` variants:
  - `MaxChunkLengthExceeded`: Security limit violation
  - `Io`: Wrapper for underlying I/O errors

### 5. Configuration Options
- Default delimiters (`DEFAULT_SEEK_DELIMITERS`, `DEFAULT_SEQUENCE_WRITER`)
- Constructor variants (`new`, `new_with_max_length`)

## Integration with Project
- Part of Tokio's utilities for stream processing
- Complements other codecs in `tokio_util::codec`
- Enables flexible message framing for network protocols
- Used with Tokio's I/O primitives through `Decoder`/`Encoder` traits

## Example Usage
```rust
let mut codec = AnyDelimiterCodec::new(b",;\r\n".to_vec(), b";".to_vec());
let mut buf = BytesMut::from("chunk 1,chunk 2;chunk 3\n\r");
assert_eq!("chunk 1", codec.decode(&mut buf).unwrap().unwrap());
```

## Safety Features
- Configurable maximum chunk length prevents memory exhaustion
- Automatic recovery from oversized chunk scenarios
- Default safe configuration with common delimiters
