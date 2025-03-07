# SplitStream in tokio-stream

## Purpose
The `SplitStream` struct is a wrapper around Tokio's `tokio::io::Split` type, enabling it to implement the `Stream` trait. This allows asynchronous iteration over byte segments split by a delimiter (e.g., newline characters) from an `AsyncBufRead` source (e.g., a buffered reader).

## Key Components

### Struct Definition
- **`SplitStream<R>`**: Wraps `tokio::io::Split<R>` where `R: AsyncBufRead`.
  - Uses `pin_project!` to safely handle pinned projections for async operations.
  - Provides methods to create, unwrap, and access the inner `Split<R>`.

### Core Methods
- `new(split: Split<R>)`: Constructs a `SplitStream` from a `Split<R>`.
- `into_inner()`: Recovers the original `Split<R>`.
- `as_pin_mut()`: Grants pinned mutable access to the inner `Split<R>`.

### Stream Implementation
- Implements `Stream<Item = io::Result<Vec<u8>>>` for `SplitStream<R>`.
- **`poll_next`**: Asynchronously polls the next byte segment using `poll_next_segment` from `Split<R>`. The `transpose` method converts `Result<Option<T>>` to `Option<Result<T>>` to match the `Stream` interface.

### Interoperability
- Implements `AsRef<Split<R>>` and `AsMut<Split<R>>` to expose the inner `Split<R>` for direct manipulation.

## Integration with the Project
This file is part of the `tokio-stream` crate's `wrappers` module, which provides adapters to convert Tokio I/O primitives into `Stream`-compatible types. It bridges Tokio's asynchronous I/O utilities (like splitting buffers) with the `Stream` abstraction, enabling seamless use in stream-based pipelines (e.g., processing lines from a file or network socket).

---
