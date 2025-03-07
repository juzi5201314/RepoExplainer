# Tokio Context Utilities

## Purpose
This module provides utilities for running Tokio-specific futures on non-Tokio executors by preserving their runtime context. It enables interoperability between Tokio and other async runtimes by allowing futures to retain access to Tokio runtime features (e.g., timers, I/O) even when executed outside a Tokio runtime.

## Key Components

### `TokioContext<F>` Struct
A wrapper around a future `F` that associates it with a Tokio runtime via a [`Handle`](https://docs.rs/tokio/latest/tokio/runtime/struct.Handle.html). Key features:
- **Runtime Context Preservation**: Uses `handle.enter()` in its `poll` method to ensure the wrapped future executes within the correct Tokio context.
- **Lifetime Management**: Requires the underlying `Runtime` to stay alive while the future is executing.
- **API Methods**:
  - `new()`: Associates a future with a runtime handle.
  - `handle()`: Returns a reference to the stored handle.
  - `into_inner()`: Extracts the inner future, removing the runtime association.

### `RuntimeExt` Trait
An extension trait for `tokio::runtime::Runtime` that simplifies context wrapping:
- **`wrap()` Method**: Creates a `TokioContext` directly from a runtime instance, bundling its handle with a future.

## Implementation Details
- **Future Polling**: The `poll` method of `TokioContext` enters the runtime context before delegating to the inner future's polling logic.
- **Safety Considerations**: Warns against using `current_thread` runtime due to potential context entry requirements. Recommends multi-threaded runtime even with a single worker thread.

## Integration with Project
This file addresses cross-runtime compatibility in the `tokio-util` crate. It bridges Tokio-specific features (e.g., timers, I/O) with non-Tokio executors, enabling use cases like:
- Running Tokio-based libraries (e.g., `tokio::time::sleep`) in alternative async runtimes.
- Mixing Tokio and non-Tokio components in hybrid applications.

## Example Usage
```rust
// Wrap a Tokio future (e.g., sleep) and execute it on a non-Tokio runtime:
let rt_with_timer = tokio::runtime::Runtime::new().unwrap();
let rt_without_timer = tokio::runtime::Runtime::new().unwrap();

let wrapped_future = rt_with_timer.wrap(async {
    tokio::time::sleep(Duration::from_secs(1)).await
});

rt_without_timer.block_on(wrapped_future); // Executes with timer support
```

## Related Context
The code interacts with other Tokio utilities like async I/O adapters and compatibility layers for `futures-io`, but focuses specifically on runtime context propagation rather than direct I/O operations.

---
