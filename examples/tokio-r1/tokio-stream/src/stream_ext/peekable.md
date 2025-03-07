# Tokio Stream `peekable.rs` Explanation

## Purpose
This file implements a `Peekable` stream adapter for Tokio's asynchronous streams. It enables lookahead functionality, allowing users to inspect the next item in a stream without consuming it immediately. This is analogous to the standard library's `Peekable` iterator but designed for async streams.

## Key Components

### 1. `Peekable` Struct
```rust
pub struct Peekable<T: Stream> {
    peek: Option<T::Item>,
    #[pin]
    stream: Fuse<T>,
}
```
- **`peek`**: Stores the lookahead item when available
- **`stream`**: Underlying fused stream (wrapped in `Fuse` to guarantee termination after `None`)

### 2. Core Functionality
- **`new()`**: Initializes the peekable stream with a fused base stream
- **`peek()` async method**:
  - Returns a reference to the next item
  - Buffers the next item if not already peeked
  - Works with `Unpin` streams for safe async access

### 3. Stream Implementation
```rust
impl<T: Stream> Stream for Peekable<T> {
    fn poll_next(...) -> Poll<Option<Self::Item>> {
        // Returns peeked item if available, 
        // otherwise polls underlying stream
    }
}
```
- Prioritizes returning buffered peeked items
- Delegates to wrapped stream when no peeked item exists

## Integration with Project
- Part of `StreamExt` extension traits in Tokio
- Uses `Fuse` from `stream_ext` to safely handle stream termination
- Follows Tokio's pinning patterns for safe async operations
- Complements other stream adapters (fuse, pending, etc.) shown in related context

## Behavioral Notes
- Peeked items are consumed on subsequent `poll_next` calls
- Maintains stream fusion to prevent post-termination items
- Designed for zero-cost abstraction where possible
