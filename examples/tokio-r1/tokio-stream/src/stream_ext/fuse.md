# `fuse.rs` in Tokio Streams

## Purpose
Provides the `Fuse` stream adapter that ensures a stream permanently stops after emitting `None`. This prevents streams from being polled again after termination, enforcing termination guarantees in async Rust.

## Key Components

### `Fuse` Struct
```rust
pub struct Fuse<T> {
    stream: Option<T>,
}
```
- Wraps an inner stream in `Option` to track its lifecycle.
- Uses `pin_project!` macro to safely handle pinned projections of the stream.

### Core Implementation
1. **Construction**:
   - `new(stream: T)` initializes with an active stream wrapped in `Some`.

2. **Stream Trait**:
   - **`poll_next`**: 
     - Polls the inner stream while active (`Some`).
     - Sets the inner stream to `None` upon receiving `Poll::Ready(None)`, preventing future polls.
   - **`size_hint`**:
     - Delegates to the inner stream's hint when active.
     - Returns `(0, Some(0))` after termination to indicate completion.

## Behavior
- **Termination Enforcement**: Once the inner stream signals completion (`None`), `Fuse` guarantees all subsequent polls return `Poll::Ready(None)`.
- **Safety**: Uses pinning (`pin_project_lite`) to ensure memory safety when projecting pinned streams.

## Integration
- Part of `StreamExt` trait's `fuse()` method.
- Works with other stream utilities (e.g., `Iter`, `Pending`, `Once`) shown in related context.
- Ensures streams adhere to termination semantics required by combinators and consumers.

---
