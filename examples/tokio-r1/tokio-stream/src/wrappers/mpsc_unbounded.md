# `mpsc_unbounded.rs` Explanation

## Purpose
This file provides a wrapper around Tokio's `UnboundedReceiver` to implement the `Stream` trait, enabling asynchronous iteration over messages received through an unbounded multi-producer single-consumer channel.

## Key Components

### 1. `UnboundedReceiverStream` Struct
- **Wrapper Type**: Contains an `UnboundedReceiver<T>` as its `inner` field
- **Stream Conversion**: Bridges Tokio's channel receiver with the Stream API
- **Additional Methods**:
  - `new()`: Creates wrapper from `UnboundedReceiver`
  - `into_inner()`: Recovers original receiver
  - `close()`: Gracefully closes channel while draining messages

### 2. Core Implementations
- **`Stream` Trait**:
  - Implements async polling via `poll_next` using the receiver's native `poll_recv`
  - Enables use with Stream combinators (`next()`, `map()`, etc.)
- **Conversion Traits**:
  - `From<UnboundedReceiver>` for seamless conversion
  - `AsRef/AsMut` for accessing underlying receiver
- **Thread Safety**: Inherits thread-safe properties from Tokio's MPSC channel

### 3. Documentation
- Includes practical example showing:
  - Channel creation
  - Message sending
  - Stream consumption pattern
  - Proper cleanup handling

## Project Integration
- Part of `tokio-stream`'s adapter utilities
- Enables interoperability between Tokio's synchronization primitives and Stream-based APIs
- Complements other channel wrappers (like bounded channel adapters) in the crate
