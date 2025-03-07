# `watch.rs` Explanation

## Purpose
This file implements a `WatchStream` wrapper around Tokio's `watch::Receiver` to convert it into a [`Stream`](https://docs.rs/futures/latest/futures/stream/trait.Stream.html) that yields values when they change. It provides two construction patterns:
1. Immediate emission of current value
2. Emission only on subsequent changes

## Key Components

### 1. Core Structure
```rust
pub struct WatchStream<T> {
    inner: ReusableBoxFuture<'static, (Result<(), RecvError>, Receiver<T>)>,
}
```
Uses `ReusableBoxFuture` to manage the asynchronous state machine efficiently while handling value changes.

### 2. Construction Methods
- `new()`: Immediately returns current value on first poll
- `from_changes()`: Waits for first change before yielding values

### 3. Stream Implementation
```rust
impl<T: Clone + 'static + Send + Sync> Stream for WatchStream<T> {
    type Item = T;

    fn poll_next(...) -> Poll<Option<Self::Item>> {
        // Handles value updates and error states
    }
}
```
Manages the polling lifecycle:
1. Waits for receiver change notification
2. Clones updated value
3. Resets future for next change

### 4. Error Handling
- Converts `RecvError` (sender closed) into stream termination
- Properly cleans up resources on errors

## Integration with Project
This wrapper bridges Tokio's watch channels with the standard Stream interface, enabling:
- Seamless use in async/await contexts
- Composition with other stream combinators
- Integration with ecosystem components expecting Stream inputs

## Example Usage Patterns
```rust
// Immediate value + changes
let mut stream = WatchStream::new(rx);

// Changes-only mode
let mut stream = WatchStream::from_changes(rx);
```

## Design Considerations
- Zero-cost abstraction using Tokio's primitives
- Memory efficiency through clone-on-change
- Thread-safe implementation (Send + Sync bounds)
- Proper handling of backpressure through Stream semantics
