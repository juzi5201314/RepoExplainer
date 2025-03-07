# Tokio I/O Interest Module

## Purpose
The `interest.rs` file defines the `Interest` type and related operations for specifying I/O readiness events in Tokio's asynchronous I/O system. It acts as an abstraction layer between Tokio's high-level event interests and platform-specific system calls (via Mio).

## Key Components

### Bitmask Constants
- Platform-specific event flags (`READABLE`, `WRITABLE`, `AIO`, `LIO`, `PRIORITY`, `ERROR`)
- Values correspond to Mio's event system but add Tokio-specific extensions
- ERROR (0b0010_0000) is unique to Tokio for error event tracking

### Interest Struct
```rust
pub struct Interest(usize);
```
- Wraps a bitmask of event interests
- Provides type-safe operations for event interest composition

### Core Functionality
1. **Interest Composition**:
   - `add()`/`remove()` methods for combining interests
   - Bitwise operator implementations (`BitOr`, `BitOrAssign`)
   - Platform-specific interests (AIO/LIO for FreeBSD, PRIORITY for Linux)

2. **Conversion Logic**:
   - `to_mio()` converts to Mio's Interest type
   - Handles platform-specific mapping and error interest conversion
   - Maintains compatibility with Mio's event system

3. **Event Masking**:
   - `mask()` method returns corresponding `Ready` flags
   - Maps interests to concrete readiness states (including closed events)

### Platform Handling
- Conditional compilation for:
  - FreeBSD (AIO/LIO)
  - Linux/Android (PRIORITY)
  - Error handling differences across platforms
- Documentation cfg attributes for cross-platform clarity

## Integration with Project
- Works with `Ready` type from sibling module
- Used by I/O driver for event registration
- Forms base of Tokio's async I/O primitives (TCP, UDP, files)
- Abstracts platform differences in event notification systems

## Key Methods
- `is_*()` checkers: Test interest presence
- `add()`/`remove()`: Modify interest sets
- `to_mio()`: Bridge to underlying I/O library
- `mask()`: Convert to observable readiness states

```rust
// Example usage
let interests = Interest::READABLE.add(Interest::WRITABLE);
if interests.is_readable() {
    // Handle read readiness
}
```

## Debug Representation
- Human-readable format showing active interests:
  ```rust
  // Output: "READABLE | WRITABLE | PRIORITY"
  ```

This file serves as the foundation for Tokio's event-driven I/O system, translating high-level interest specifications into platform-specific event notifications.
