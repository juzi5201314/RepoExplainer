## Code File Explanation: `tokio-stream/src/stream_ext/next.rs`

### Purpose
This file defines the `Next` future type, which implements the asynchronous `next` method for streams. It allows polling a stream to retrieve its next item in a cancel-safe manner, ensuring no values are lost if the future is dropped.

### Key Components
1. **`Next` Struct**:
   - A `#[pin_project]`-pinned future that holds a mutable reference to a stream (`&'a mut St`).
   - Uses `PhantomPinned` to enforce `!Unpin` semantics, ensuring safe pinning for async compatibility.
   - Marked as `#[must_use]` to emphasize that it has no effect unless polled.

2. **Future Implementation**:
   - Implements `Future` for `Next<'_, St>` where `St` is a `Stream`.
   - The `poll` method delegates directly to the underlying stream's `poll_next`, returning `Poll<Option<St::Item>>`.

3. **Cancel Safety**:
   - The struct only holds a reference to the stream, so dropping the `Next` future does not consume or alter the stream's state.

### Integration with Project
- Part of the `StreamExt` trait extension for `Stream`s in Tokio's async ecosystem.
- Enables ergonomic stream processing via `.next().await` syntax, similar to async iterators.
- Works alongside other stream combinators (e.g., `take`, `then`, `collect`) in `stream_ext` to provide a comprehensive async stream API.

### Relationship to Context
The related code shows similar patterns for stream combinators (e.g., `Take`, `Then`), which:
- Use `pin_project!` for pinning.
- Implement `poll`/`poll_next` to delegate or transform stream outputs.
- Emphasize cancel safety and async-compatible pinning.

---
