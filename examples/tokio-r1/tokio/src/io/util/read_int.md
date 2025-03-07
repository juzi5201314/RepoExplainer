# Code File Explanation: `read_int.rs`

## Purpose
This file provides asynchronous utilities for reading primitive integer types from an `AsyncRead` source in Tokio. It handles both big-endian and little-endian formats, supporting various integer sizes (8-bit to 128-bit) and floating-point numbers.

## Key Components

### Macros
1. **`reader!` Macro**:
   - Generates `Future` implementations for multi-byte integers (16-bit to 128-bit).
   - Creates a pinned struct with:
     - A byte buffer sized for the target type
     - Tracking of bytes read
     - PhantomPinned for async safety
   - Implements async polling logic to read bytes incrementally until the full type is read.

2. **`reader8!` Macro**:
   - Specialized for 8-bit integers (u8/i8).
   - Directly reads a single byte without buffering.
   - Simpler implementation due to single-byte requirement.

### Generated Futures
- **Endian-aware readers**:
  - `ReadU16`, `ReadU32`, ..., `ReadU128` (big-endian)
  - `ReadU16Le`, `ReadU32Le`, ..., `ReadU128Le` (little-endian)
  - Corresponding signed (`ReadI*`) and float (`ReadF*`) variants
- **8-bit readers**:
  - `ReadU8` and `ReadI8` (no endian handling needed)

### Core Logic
- **Async Polling**:
  - Uses `ReadBuf` to handle partial reads
  - Accumulates bytes until the required size is reached
  - Converts bytes to target type using `bytes::Buf` methods
- **Error Handling**:
  - Returns `UnexpectedEof` if stream ends prematurely
  - Propagates I/O errors from underlying reader

## Integration with Project
- Part of Tokio's I/O utilities
- Complements similar write operations for full binary I/O support
- Used by higher-level protocols needing primitive type serialization
- Integrates with Tokio's async ecosystem via `AsyncRead` trait

## Implementation Details
- **Pinning**: Uses `pin_project_lite` and `PhantomPinned` for async safety
- **Buffer Management**: Pre-allocates fixed-size buffers for each type
- **Zero-Copy**: Leverages `bytes::Buf` for efficient byte conversion
