# Tokio-Stream Broadcast Wrapper Explanation

## Purpose
This file provides a `BroadcastStream` wrapper that adapts Tokio's `broadcast::Receiver` to implement the `futures_core::Stream` trait. It enables asynchronous consumption of broadcast channel messages through the standard Stream interface, including error handling for lagged consumers.

## Key Components

### 1. BroadcastStream Struct
- **Core Wrapper**: Contains a `ReusableBoxFuture` that manages polling of the broadcast receiver
- **Lifetime Management**: Uses `'static` lifetime to work with Tokio's async runtime
- **Type Constraints**: Requires `T: Clone + Send` to match broadcast channel semantics

### 2. Error Handling
- `BroadcastStreamRecvError` enum:
  - `Lagged(u64)`: Indicates message skipping due to slow consumption
  - Implements `Display` and `Error` for proper error reporting

### 3. Stream Implementation
- `poll_next` method:
  - Uses `ReusableBoxFuture` to manage async polling
  - Handles three states:
    1. Successful message reception (`Ok(item)`)
    2. Channel closure (`RecvError::Closed`)
    3. Lag detection (`RecvError::Lagged`)

### 4. Conversion Traits
- `From<Receiver<T>>` implementation allows seamless conversion from broadcast receivers to streams

## Integration with Project
- Part of Tokio-Stream's synchronization primitive adapters
- Complements other wrappers like `WatchStream`
- Enables interoperability between Tokio's broadcast channels and Stream-based ecosystems

## Example Usage
```rust
let (tx, rx) = broadcast::channel(16);
let mut stream = BroadcastStream::new(rx);
while let Some(item) = stream.next().await {
    match item {
        Ok(msg) => process(msg),
        Err(BroadcastStreamRecvError::Lagged(skipped)) => handle_lag(skipped),
    }
}
```
