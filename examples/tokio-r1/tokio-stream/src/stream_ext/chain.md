# Chain Stream Combinator Implementation

## Purpose
This file implements the `Chain` stream combinator, which concatenates two streams sequentially. It first yields items from the first stream, then continues with items from the second stream once the first completes.

## Key Components

### 1. `Chain` Struct
```rust
pub struct Chain<T, U> {
    a: Fuse<T>,
    b: U,
}
```
- **Fuse<T>**: Wraps the first stream to ensure it permanently returns `None` after completion.
- **U**: The second stream that continues after the first completes.

### 2. Core Implementation
- **`new` constructor**: Initializes with two streams, fusing the first.
- **Stream trait implementation**:
  - `poll_next`: First polls the fused stream `a`, then switches to `b` when `a` is exhausted.
  - `size_hint`: Combines size hints from both streams using `merge_size_hints`.

### 3. Polling Logic
```rust
fn poll_next(...) -> Poll<Option<T::Item>> {
    // First check fused stream
    if let Some(v) = ready!(me.a.poll_next(cx)) {
        return Ready(Some(v));
    }
    // Then check second stream
    me.b.poll_next(cx)
}
```
- Uses `ready!` macro to handle pending states
- Ensures strict ordering: `b` is only polled after `a` completes

## Relationship to Project
- Part of `StreamExt` extension trait in Tokio's async streams
- Follows Rust's combinator pattern similar to iterator adapters
- Integrates with other combinators like `Fuse`, `Merge`, and `Take` through shared utilities

## Design Considerations
- **Fusing**: Prevents accidental reactivation of completed streams
- **Zero-cost abstractions**: Leverages pinning for safe async handling
- **Efficient size hints**: Provides combined item count estimates
