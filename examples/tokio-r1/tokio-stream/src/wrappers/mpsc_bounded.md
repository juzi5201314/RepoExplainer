# ReceiverStream Wrapper for Bounded MPSC Channels

## Purpose
This file provides `ReceiverStream<T>`, a wrapper around Tokio's bounded MPSC (multi-producer, single-consumer) channel receiver (`tokio::sync::mpsc::Receiver`). Its primary purpose is to adapt the asynchronous receiver into a [`Stream`](https://docs.rs/futures/latest/futures/stream/trait.Stream.html), enabling compatibility with stream-processing utilities.

## Key Components

### 1. Core Struct
- **`ReceiverStream<T>`**: Wraps a `tokio::sync::mpsc::Receiver<T>` and implements the `Stream` trait. This allows iterating over received values using async stream semantics.

### 2. Key Methods
- **`new(recv: Receiver<T>)`**: Constructs a new stream wrapper from a receiver.
- **`into_inner()`**: Recovers the original `Receiver<T>`, useful for interoperability with non-stream code.
- **`close()`**: Gracefully closes the receiver, preventing new messages while allowing buffered messages to be drained.

### 3. Trait Implementations
- **`Stream`**: Delegates to `Receiver::poll_recv` to implement async iteration.
- **`AsRef`/`AsMut`**: Provides access to the inner receiver via references.
- **`From<Receiver<T>>`**: Enables type conversion for ergonomic usage (e.g., `ReceiverStream::from(rx)`).

## Integration with Project
This file is part of Tokio's stream utilities (`tokio-stream` crate), specifically in the `wrappers` module. It bridges Tokio's channel primitives with the stream ecosystem by:
1. Enabling use of MPSC receivers in stream pipelines (e.g., with `StreamExt` combinators).
2. Complementing similar wrappers (e.g., for unbounded channels) to provide consistent channel/stream interoperability.

## Example Usage
Demonstrated in the docs, a channel receiver is wrapped and used as a stream:
```rust
let (tx, rx) = mpsc::channel(2);
let mut stream = ReceiverStream::new(rx);
while let Some(item) = stream.next().await { /* ... */ }
```
