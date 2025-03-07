markup
## Code File Explanation: `tokio-stream/src/stream_ext/any.rs`

### Purpose
This file implements `AnyFuture`, a `Future` used to check if **any element** in an asynchronous stream satisfies a given predicate. It is part of the `StreamExt` trait extension for `Stream` in Tokio's async runtime, providing a non-blocking way to evaluate stream elements.

### Key Components
1. **`AnyFuture` Struct**:
   - Wraps a mutable reference to a stream (`&'a mut St`) and a predicate closure (`F`).
   - Uses `PhantomPinned` to enforce immovability (`!Unpin`), ensuring safe async behavior with pinned data.

2. **Future Implementation**:
   - The `poll` method drives the async logic:
     - Polls the stream up to **32 times** per invocation to balance throughput and fairness.
     - Applies the predicate closure to each stream item. Returns `Poll::Ready(true)` immediately if any item matches.
     - Returns `Poll::Ready(false)` if the stream ends without a match.
     - Yields control (`Poll::Pending`) after 32 iterations to avoid starvation, using `wake_by_ref()` to reschedule polling.

3. **Integration with Streams**:
   - Designed for streams implementing `Stream + Unpin`.
   - Works with generic predicates (`F: FnMut(St::Item) -> bool`), similar to `Iterator::any` but for async contexts.

### Relationship to Project
- Part of Tokio's `tokio-stream` utilities for async stream processing.
- Complements other `StreamExt` methods like `all`, `fold`, and `take`, providing a consistent API for stream operations.
- Enables ergonomic, non-blocking stream evaluation in async applications.

---
