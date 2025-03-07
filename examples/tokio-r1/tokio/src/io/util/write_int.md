## Tokio Async Integer Writers (`write_int.rs`)

### Purpose
This file provides asynchronous writers for various integer types (both signed/unsigned and different sizes) with support for big-endian and little-endian formats. These utilities enable efficient, non-blocking writes of numeric values through Tokio's `AsyncWrite` interface, handling partial writes and proper byte serialization.

### Key Components

1. **Macro Architecture**:
   - `writer!`: Generates future types for multi-byte integers (16-128 bits)
     - Creates pinned structs with buffers sized for the target type
     - Uses `BufMut` methods for proper endianness handling
     - Implements `Future` with partial write handling
   - `writer8!`: Specialized macro for 8-bit types (single-byte writes)

2. **Generated Writers**:
   - Covers all primitive integer types (u8-i128) and floats (f32/f64)
   - Provides both native-endian and explicit little-endian variants
   - Examples: `WriteU16`, `WriteI32Le`, `WriteF64`

3. **Future Implementation**:
   - Tracks written bytes using `written` counter
   - Handles partial writes through polling
   - Properly propagates IO errors and write-zero conditions
   - Ensures compatibility with async traits via `PhantomPinned`

### Integration with Tokio
- Extends Tokio's async IO capabilities with numeric serialization
- Complements other IO utilities like `WriteAll` and buffered writers
- Used internally by higher-level protocols needing binary data formatting
- Integrates with Tokio's async runtime through `AsyncWrite` trait

### Implementation Details
- Uses `pin_project` for safe pinning of async types
- Leverages `bytes::BufMut` for efficient buffer management
- Handles both big-endian (default) and little-endian formats
- Optimizes single-byte writes with direct passthrough
