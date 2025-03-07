# Tokio Join Utility

## Purpose
This file provides a mechanism to combine separate `AsyncRead` and `AsyncWrite` implementations into a single unified handle (`Join` struct). This allows treating read/write components as one entity while preserving their individual functionality.

## Key Components

### 1. `Join` Struct
- **Structure**: Contains pinned `reader` (generic `R`) and `writer` (generic `W`) fields
- **Attributes**: 
  - Implements `Debug`
  - Uses `pin_project_lite` for safe pinning of fields
- **Methods**:
  - `into_inner()`: Splits back into original components
  - Accessors (`reader()`, `writer()`, etc.): Provide various access patterns (ref/mut/pinned)

### 2. Trait Implementations
- **`AsyncRead` for Join<R,W>**:
  - Delegates `poll_read` to inner reader
- **`AsyncWrite` for Join<R,W>**:
  - Delegates write-related methods (`poll_write`, `poll_flush`, etc.) to inner writer
- **`AsyncBufRead` for Join<R,W>**:
  - Delegates buffered read operations to inner reader

### 3. Factory Function
- `join()`: Creates a `Join` instance from reader/writer pair

## Integration with Project
- Part of Tokio's I/O abstraction layer
- Enables composition of I/O components (e.g., combining split stream halves)
- Works with other async I/O primitives (`AsyncRead`, `AsyncWrite`) in the ecosystem
- Complements similar utilities like `Chain` and `Either` for I/O handling

## Design Considerations
- Maintains separation of concerns while providing unified interface
- Uses pinning for async safety with self-referential structs
- Preserves full access to underlying components when needed
