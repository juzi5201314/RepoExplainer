## Code Explanation: `try_next.rs` in Tokio Stream

### Purpose
This file implements the `TryNext` future type for the `try_next` method in Tokio's `StreamExt` trait. Its primary role is to safely asynchronously retrieve the next `Result`-wrapped item from a stream while propagating errors and maintaining cancellation safety.

### Key Components

1. **`TryNext` Struct**:
   - A pinned, `!Unpin` future that wraps an inner `Next` future (from the same module).
   - Uses `PhantomPinned` to enforce immovability, ensuring async safety.
   - Derives cancellation safety by holding only a reference to the underlying stream.

2. **Future Implementation**:
   - Polls the inner `Next` future to get an `Option<Result<T, E>>`.
   - Transposes the result using `Option::transpose` to convert:
     - `Some(Ok(T))` → `Ok(Some(T))`
     - `Some(Err(E))` → `Err(E)`
     - `None` → `Ok(None)`
   - This matches Rust's error-handling patterns (similar to the `?` operator).

3. **Integration with Streams**:
   - Works with streams of type `Stream<Item = Result<T, E>>`.
   - Enables error-aware iteration over streams, stopping on the first error.

### Relationship to Project
- Part of Tokio's stream utilities (`stream_ext` module).
- Complements other combinators like `Next`, `Collect`, and `Take` by adding error propagation.
- Used in async contexts where streams may produce recoverable/unrecoverable errors.

---
