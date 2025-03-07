# IntervalStream Wrapper Explanation

## Purpose
The `IntervalStream` struct wraps Tokio's `Interval` type to implement the `Stream` trait, enabling periodic time intervals to be consumed as an asynchronous stream of `Instant` values. This bridges Tokio's timer functionality with stream processing capabilities.

## Key Components

### Struct Definition
- **`IntervalStream`**: Contains an inner `tokio::time::Interval`.
- Implements `Debug` for diagnostics.
- Marked with `doc(cfg(feature = "time"))` for conditional documentation.

### Core Methods
- **`new(interval: Interval)`**: Constructs a stream from an existing `Interval`.
- **`into_inner()`**: Recovers the original `Interval` from the wrapper.

### Stream Implementation
- **`poll_next`**: Delegates to `Interval::poll_tick()`, emitting `Some(Instant)` on each interval tick.
- **`size_hint`**: Returns `(usize::MAX, None)`, indicating an unbounded stream.

### Interoperability Traits
- **`AsRef<Interval>`** and **`AsMut<Interval>`**: Allow direct access to the underlying `Interval` for advanced use cases.

## Example Usage
```rust
let interval = tokio::time::interval(Duration::from_millis(10));
let mut stream = IntervalStream::new(interval);
while let Some(instant) = stream.next().await {
    // Handle periodic event
}
```

## Project Role
This wrapper integrates Tokio's timer system with the stream ecosystem, enabling interval-based operations in stream pipelines (e.g., timeouts, throttling). It serves as an adapter between low-level timing primitives and higher-level stream processing utilities.

---
