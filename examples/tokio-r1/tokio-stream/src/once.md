# Code File Explanation: `tokio-stream/src/once.rs`

## Purpose
This file defines the `Once<T>` stream and its associated `once` function, which creates a stream that emits a single value exactly once before terminating. It is a foundational utility for converting a single value into an asynchronous stream compatible with Tokio's streaming ecosystem.

## Key Components

### 1. **`Once<T>` Struct**
- **Role**: Represents a stream that emits a single value of type `T`.
- **Structure**: Wraps an `Iter<option::IntoIter<T>>`, leveraging Tokio's existing iterator-to-stream adapter (`Iter`) to handle polling logic.
- **Attributes**:
  - `#[derive(Debug)]`: Enables debugging.
  - `#[must_use]`: Ensures the stream is actively polled, as streams have no effect until polled.

### 2. **`once` Function**
- **Signature**: `pub fn once<T>(value: T) -> Once<T>`
- **Behavior**: Constructs a `Once` stream by wrapping the provided `value` in an `Option`, converting it into an iterator, and then into a stream via `crate::iter`.
- **Example**:
  ```rust
  let mut one = stream::once(1);
  assert_eq!(Some(1), one.next().await); // Emits `1` once.
  ```

### 3. **`Stream` Trait Implementation**
- **`poll_next` Method**: Delegates to the inner `Iter` stream's `poll_next`, allowing the stream to emit its single value and then return `Poll::Ready(None)`.
- **`size_hint` Method**: Propagates the size hint from the inner iterator, ensuring accurate bounds (e.g., `(1, Some(1))` for a single item).

## Integration with the Project
- **Reusability**: The `Once` stream reuses the `Iter` adapter from Tokio's stream utilities, minimizing redundancy.
- **Consistency**: Follows patterns seen in other stream types (e.g., `Empty`, `Pending`, `Iter`), ensuring a uniform API.
- **Use Case**: Useful in scenarios requiring a single-value stream, such as mocking, testing, or bridging synchronous values into asynchronous pipelines.

## Related Context
- The `once` stream complements other utilities like `iter` (for converting iterators to streams) and `empty` (for creating empty streams).
- Similar patterns appear in other stream implementations (e.g., `Pending`, `Spawn`, `TimeoutRepeating`), where delegation to inner streams or futures is common.

---
