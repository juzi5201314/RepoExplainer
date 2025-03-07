markup
# empty.rs - Tokio Stream Empty Implementation

## Purpose
Provides an `Empty` stream implementation that immediately completes without yielding any elements. This serves as a fundamental utility for creating placeholder/completed streams in asynchronous Rust programming.

## Key Components

### `Empty<T>` Struct
- Generic struct using `PhantomData<T>` to maintain type safety without storing actual data
- Marked `#[must_use]` to warn about unused streams
- Implements thread safety traits (`Send`, `Sync`) and `Unpin`

### Constructor Function
- `pub const fn empty<T>() -> Empty<T>`: Creates a zero-sized stream instance at compile time

### Stream Implementation
- Implements `Stream` trait with:
  - `poll_next()`: Always returns `Poll::Ready(None)` indicating immediate completion
  - `size_hint()`: Returns (0, Some(0)) indicating zero elements

## Key Characteristics
- Immediately terminates when polled
- Zero-sized implementation (no heap allocation)
- Thread-safe and movable between threads
- Constant-time constructor

## Relationship to Project
- Contrasts with `pending()` stream that never yields
- Part of core stream primitives in `tokio-stream`
- Used as a building block for stream combinators and control flow
- Provides equivalent functionality to `futures::stream::empty` in Tokio ecosystem

## Example Usage
```rust
let mut none = stream::empty::<i32>();
assert_eq!(None, none.next().await);  // Immediately returns None
```

## Integration with Other Components
- Shares trait implementations with other stream types (`Pending`, `ReceiverStream`, etc.)
- Follows same pattern as other stream utilities in the crate (struct + constructor + trait impl)
- Used in scenarios requiring placeholder streams or completed stream signals
