# UnixListenerStream Explanation

## Purpose
This file implements a wrapper around Tokio's `UnixListener` to make it conform to the `Stream` trait, enabling asynchronous iteration over incoming Unix domain socket connections.

## Key Components

### 1. Struct Definition
- `UnixListenerStream`: Main wrapper struct containing a `UnixListener`
- Implements `Debug` and conditional documentation attributes for Unix/net feature

### 2. Core Functionality
- `new()`: Creates wrapper from existing listener
- `into_inner()`: Recovers original listener
- `Stream` implementation: Polls for incoming connections using `poll_accept`
  - Yields `UnixStream` instances or errors
  - Returns `Poll::Pending` when no connections are ready

### 3. Compatibility Traits
- `AsRef`/`AsMut` implementations: Allow direct access to underlying listener
- Maintains compatibility with standard listener operations

## Integration with Project
Part of Tokio's network utilities, providing:
- Consistent Stream interface across different listener types (TCP/Unix)
- Enables async/await syntax for connection handling
- Complements similar implementations for TCP listeners

## Example Usage
```rust
let listener = UnixListener::bind("/tmp/sock")?;
let mut incoming = UnixListenerStream::new(listener);

while let Some(stream) = incoming.next().await {
    // Handle connection
}
```

## Design Considerations
- Preserves direct access to underlying listener
- Handles both successful connections and errors in polling
- Maintains zero-cost abstraction principles
