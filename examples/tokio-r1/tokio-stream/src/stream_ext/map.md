### Code File Explanation: `tokio-stream/src/stream_ext/map.rs`

#### Purpose
This file defines the `Map` stream adapter, which implements the `map` method for transforming items emitted by an asynchronous stream. It is part of Tokio's stream utilities, enabling functional-style transformations on streams.

#### Key Components
1. **Struct `Map<St, F>`**:
   - Wraps an underlying stream `St` and a mapping function `F`.
   - Uses `pin_project!` to safely handle pinned projections for async operations.
   - Marked `#[must_use]` to emphasize that it has no effect unless polled.

2. **Trait Implementations**:
   - **`Debug`**: Conditionally implemented if the wrapped stream `St` supports `Debug`.
   - **`Stream`**: Core implementation for the adapter:
     - **`poll_next`**: Polls the underlying stream and applies the function `F` to each item.
     - **`size_hint`**: Delegates to the wrapped stream's hint, preserving size metadata.

3. **Constructor**:
   - `new(stream: St, f: F)`: Creates a `Map` instance (internal to the crate).

#### Implementation Details
- **Polling Behavior**: When polled, the adapter delegates to the wrapped stream's `poll_next`, then maps the result using `F`. The transformation is applied lazily as items are produced.
- **Zero-Cost Abstraction**: Avoids overhead by deferring execution of `F` until items are emitted, matching Rust's iterator conventions.

#### Relationship to Project
- Part of the `StreamExt` trait extensions in Tokio, providing chainable methods for stream manipulation.
- Follows the same pattern as other adapters (e.g., `Take`, `FilterMap`), wrapping streams to modify their behavior.
- Enables functional programming patterns for asynchronous data processing (e.g., `stream.map(|x| x * 2)`).

#### Example Flow
1. A user calls `.map(f)` on a stream.
2. The `Map` adapter is created, wrapping the original stream and `f`.
3. During polling, each item from the underlying stream is passed through `f` before being emitted.

---
