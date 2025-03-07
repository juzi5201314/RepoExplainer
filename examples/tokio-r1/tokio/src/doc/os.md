# Tokio Windows Platform-Specific Extensions

## Purpose
This file provides Windows-specific extensions to Tokio's I/O primitives, mirroring `std::os::windows` functionality while integrating with Tokio's asynchronous runtime. It defines interfaces for raw handle/socket management and ownership semantics in an async context.

## Key Components

### Module Structure
- **`windows` module**: Top-level container for Windows-specific extensions.
  - **`io` submodule**: Focused on I/O abstractions for handles and sockets.

### Core Types & Traits
1. **Handle/Socket Types**:
   - `RawHandle`/`RawSocket`: Opaque types representing low-level Windows resources.
   - `OwnedHandle`: Owned wrapper for handles with RAII semantics.
   - `BorrowedHandle`/`BorrowedSocket`: Borrowed references with lifetime tracking.

2. **Conversion Traits**:
   - `AsRawHandle`/`AsRawSocket`: Convert objects to raw OS resources.
   - `FromRawHandle`/`FromRawSocket`: Construct objects from raw resources (unsafe).
   - `IntoRawSocket`: Consume objects to extract raw sockets.
   - `AsHandle`/`AsSocket`: Get borrowed references to resources.

### Safety Patterns
- Explicit unsafe blocks in `FromRaw*` traits highlight ownership boundary crossings.
- Lifetime parameters in `Borrowed*` types prevent dangling references.

## Integration with Tokio
- Works with `PollEvented` for async event notification.
- Enables interoperability between Tokio's async I/O (via `AsyncRead`/`AsyncWrite`) and Windows native handles.
- Provides foundation for Windows-specific async primitives like named pipes.

## Relationship to Standard Library
- Mirrors `std::os::windows::io` interface but adapted for async usage.
- Maintains compatibility through type aliases (e.g., `RawHandle` matches std's definition).
