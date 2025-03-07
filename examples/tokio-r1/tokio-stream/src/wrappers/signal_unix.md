# SignalStream in tokio-stream

## Purpose
The `signal_unix.rs` file provides a `SignalStream` struct that wraps Tokio's Unix `Signal` type to implement the `Stream` trait. This allows Unix signals (e.g., `SIGHUP`) to be processed as asynchronous streams, enabling integration with Tokio's streaming ecosystem.

## Key Components

### Struct `SignalStream`
- **Wrapper**: Contains an `inner: Signal` field, wrapping Tokio's Unix signal handler.
- **Methods**:
  - `new(signal: Signal)`: Creates a stream from a `Signal`.
  - `into_inner()`: Returns the inner `Signal`, allowing direct access if needed.

### Stream Implementation
- Implements `Stream<Item = ()>`, where each stream item indicates a received signal.
- `poll_next()` delegates to `Signal::poll_recv()`, checking for new signals in a non-blocking manner.

### Trait Implementations
- `AsRef<Signal>` and `AsMut<Signal>`: Allow access to the underlying `Signal` via references or mutable references.

## Usage Example
```rust
let signals = signal(SignalKind::hangup())?;
let mut stream = SignalStream::new(signals);
while stream.next().await.is_some() {
    println!("hangup signal received");
}
```
This listens for `SIGHUP` signals and prints a message each time one is received.

## Integration with Project
- Part of `tokio-stream`'s wrappers that adapt Tokio primitives (e.g., signals, timers, I/O) into `Stream` interfaces.
- Works alongside other wrappers like `CtrlCStream`, `IntervalStream`, and network listeners (TCP/Unix).
- Enables consistent stream-based event handling across different asynchronous sources.

## Platform & Feature Constraints
Conditionally compiled for Unix systems (`cfg(all(unix, feature = "signal"))`), ensuring platform-specific functionality is properly gated.

---
