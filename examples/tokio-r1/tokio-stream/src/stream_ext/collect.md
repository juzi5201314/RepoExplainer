## Code Explanation: `tokio-stream/src/stream_ext/collect.rs`

### Purpose
This file implements the asynchronous `collect` method for streams in Tokio, allowing items from a `Stream` to be accumulated into a collection (e.g., `Vec`, `String`, `Result`). It defines the `Collect` future and the sealed `FromStream` trait to enable type-safe collection operations.

### Key Components

1. **`Collect` Future**:
   - A pinned, `!Unpin` future returned by `StreamExt::collect`.
   - Contains:
     - The source `stream` (pinned).
     - An intermediate `collection` of type `U::InternalCollection`.
     - `PhantomPinned` to enforce pinning for async compatibility.

2. **`FromStream` Trait**:
   - A sealed trait (private implementation details) that defines:
     - `initialize`: Creates an empty collection.
     - `extend`: Adds an item to the collection.
     - `finalize`: Converts the intermediate collection to the final type.
   - Implemented for:
     - `()` (no-op collection)
     - `String` (collects string slices)
     - `Vec<T>` (collects items into a vector)
     - `Box<[T]>` (collects into a boxed slice)
     - `Result<U, E>` (collects `Result` items, short-circuiting on errors)

3. **Future Implementation**:
   - The `poll` method drives the collection process:
     - Continuously polls the stream for items.
     - Uses `FromStream::extend` to add items to the collection.
     - Stops and returns the finalized collection when the stream ends or `extend` returns `false`.

### Integration with Project
- Part of Tokio's stream utilities (`StreamExt` extension trait).
- Works with other stream combinators (e.g., `take`, `fold`, `then` shown in related context).
- Enables ergonomic conversion of streams into common Rust types via async/await syntax.

### Example Flow
1. A user calls `stream.collect::<Vec<_>>()`.
2. The `Collect` future is created with a `Vec`-backed internal collection.
3. As the stream is polled, items are pushed into the vector.
4. When the stream ends, the finalized `Vec` is returned.

---
