# Tokio Stream `map_while` Combinator Implementation

## Purpose
This file implements the `MapWhile` stream combinator for the Tokio ecosystem. It enables transforming elements of a stream using a provided function, with the ability to terminate the stream early if the function returns `None`. This is part of the `StreamExt` trait extensions for enhanced stream processing.

## Key Components

### `MapWhile` Struct
- **Definition**: A pinned-projected struct wrapping an inner stream `St` and a closure `F`.
- **Generics**:
  - `St`: The underlying stream.
  - `F`: A closure that maps stream items to `Option<T>`, where `None` stops the stream.
- **Attributes**: Marked `#[must_use]` to enforce usage when created.

### Methods
1. **Constructor**:
   - `new(stream: St, f: F)`: Creates a `MapWhile` instance. Limited to the parent module (`pub(super)`).

2. **Debug Implementation**:
   - Formats the struct for debugging, omitting the closure `F` (non-debuggable).

3. **Stream Implementation**:
   - **`poll_next`**: Polls the inner stream, applies `F` to each item. If `F` returns `None`, the stream terminates.
   - **`size_hint`**: Provides a size hint where the lower bound is `0` (due to possible early termination) and the upper bound matches the inner stream.

## Integration with the Project
- Part of the `tokio-stream` crate's combinator utilities.
- Follows patterns seen in other combinators like `TakeWhile`, `Map`, and `SkipWhile` (referenced in related context).
- Enables chaining stream operations (e.g., processing elements until a condition fails).

## Differences from Similar Combinators
- **vs `TakeWhile`**: `TakeWhile` stops based on a predicate, while `MapWhile` transforms items and uses `Option<T>` to control termination.
- **vs `Map`**: Standard `Map` always continues; `MapWhile` can halt the stream via `None`.

## Role in the Project
Implements the `map_while` method for streams, allowing element transformation with optional early termination. This combinator enhances stream processing flexibility in asynchronous Rust applications.

---
