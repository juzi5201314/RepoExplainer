# Throttle Stream Implementation

## Purpose
The `throttle.rs` file implements a stream combinator that enforces a minimum delay between consecutive items emitted by a stream. This is useful for rate-limiting or slowing down fast streams to prevent resource exhaustion or comply with external API constraints.

## Key Components

### `throttle` Function
- **Entry Point**: Creates a `Throttle` struct wrapping an input stream and initializing a delay mechanism.
- **Parameters**: 
  - `duration`: Minimum delay between items.
  - `stream`: The underlying stream to throttle.

### `Throttle` Struct
- **Fields**:
  - `delay`: A `tokio::time::Sleep` future tracking the current throttling delay
  - `duration`: Fixed delay duration between items
  - `has_delayed`: State flag indicating if the current delay has completed
  - `stream`: The wrapped input stream
- **Pin Safety**: Uses `pin_project!` macro to handle pinning of nested streams

### Core Logic (`poll_next`)
1. **Initial Delay Check**: 
   - Waits for the initial delay if not already completed (`has_delayed` flag)
2. **Stream Polling**:
   - Polls the underlying stream for the next item
3. **Reset Mechanism**:
   - After emitting an item, resets the delay timer
   - Updates state flags to enforce next delay

### Helper Methods
- `get_ref()`, `get_mut()`, `into_inner()`: Provide access to the wrapped stream
- `is_zero()`: Optimization check for zero-duration throttling

## Integration with Project
- Part of `tokio-stream`'s stream extension utilities
- Complements other stream combinators like `timeout` and `timeout_repeating`
- Used via `StreamExt` trait to enable method chaining:
  ```rust
  stream.throttle(Duration::from_secs(1))
  ```

## Example Usage
```rust
let throttled = futures::stream::repeat("data")
    .throttle(Duration::from_secs(2));
// Emits items with 2-second gaps between them
```
