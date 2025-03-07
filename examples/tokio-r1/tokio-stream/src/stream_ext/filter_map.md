### Code File Explanation: `tokio-stream/src/stream_ext/filter_map.rs`

#### Purpose
This file implements the `FilterMap` stream adapter, which combines filtering and mapping operations on a stream. It is part of Tokio's asynchronous stream utilities, enabling developers to transform and filter stream elements in a single operation.

#### Key Components
1. **Struct Definition**:
   - `FilterMap<St, F>`: A pinned-projection struct containing:
     - `stream`: The underlying stream (`St`) being processed.
     - `f`: A closure (`F`) that maps input items to optional output items (filtering by returning `None`).

2. **Debug Implementation**:
   - Provides debug formatting for `FilterMap`, excluding the closure `f` (since closures are typically not `Debug`).

3. **Constructor**:
   - `new(stream: St, f: F)`: Creates a `FilterMap` instance. Marked `pub(super)` to restrict usage to internal crate methods.

4. **Stream Implementation**:
   - Implements the `Stream` trait for `FilterMap`:
     - **`poll_next`**: Asynchronously polls the underlying stream. For each item:
       - Applies the closure `f` to the item.
       - Returns `Poll::Ready(Some(e))` if `f(e)` produces `Some(e)`, otherwise continues polling.
       - Propagates termination when the underlying stream ends.
     - **`size_hint`**: Returns `(0, upper_bound)` since the closure may filter out all items (lower bound is unknown).

#### Integration with the Project
- Part of the `StreamExt` extension trait, enabling method chaining like `stream.filter_map(|x| ...)`.
- Follows the same pattern as other stream adapters (e.g., `Map`, `Filter`, `Take`), which wrap streams with custom polling logic.
- Works with Tokio's asynchronous runtime to process streams efficiently without blocking.

#### Role in the Project