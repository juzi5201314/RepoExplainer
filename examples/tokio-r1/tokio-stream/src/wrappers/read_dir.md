# ReadDirStream Wrapper

## Purpose
This file provides `ReadDirStream`, a wrapper around Tokio's `tokio::fs::ReadDir` type, enabling it to implement the `Stream` trait from the `tokio-stream` crate. It bridges Tokio's directory iteration API with the stream abstraction for asynchronous processing.

## Key Components

### 1. Struct Definition
- **`ReadDirStream`**: Contains an inner `ReadDir` (Tokio's directory iterator). It adds `Stream` compatibility while preserving access to the original type.

### 2. Core Implementations
- **`Stream` Trait**: Implements `poll_next` using `ReadDir::poll_next_entry`, converting the result to match the `Stream` interface via `Result::transpose`.
- **Conversion Methods**:
  - `new()`: Creates a `ReadDirStream` from a `ReadDir`.
  - `into_inner()`: Recovers the original `ReadDir` if needed.
- **Interoperability**:
  - `AsRef<ReadDir>` and `AsMut<ReadDir>`: Allow direct access to the underlying `ReadDir` without ownership transfer.

### 3. Example Usage
Demonstrates streaming directory entries using `ReadDirStream` with `StreamExt`:
```rust
let dirs = read_dir(".").await?;
let mut dirs = ReadDirStream::new(dirs);
while let Some(dir) = dirs.next().await { /* ... */ }
```

## Integration with Project
- Part of the `tokio-stream` crate's `wrappers` module, which adapts Tokio types to work with `Stream`.
- Enables composition with stream utilities (e.g., filters, mappers) from `tokio-stream`.
- Conditionally compiled with `docsrs` annotations to indicate dependency on the `fs` feature.

## Role in the Project