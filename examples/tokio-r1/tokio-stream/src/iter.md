# Code File Explanation: `tokio-stream/src/iter.rs`

## Purpose
This file provides an adapter to convert a Rust `Iterator` into a Tokio `Stream`, enabling asynchronous iteration over values. It bridges synchronous iterators with asynchronous workflows by yielding items incrementally while allowing cooperative scheduling.

## Key Components

### `Iter<I>` Struct
- **Fields**:
  - `iter`: The underlying iterator producing values.
  - `yield_amt`: A counter to enforce periodic yielding (after 32 items) to avoid monopolizing the async runtime.
- Attributes:
  - `#[must_use]`: Ensures the stream is actively polled to produce values.
  - `Unpin` implementation: Allows safe use in async contexts where pinned types are required.

### `iter` Function
- Converts an `IntoIterator` into an `Iter` stream.
- Initializes `yield_amt` to 0 to start yielding immediately.

### `Stream` Trait Implementation
- **Method `poll_next`**:
  - Checks `yield_amt` to enforce cooperative yielding every 32 items.
  - Wakes the task context to reschedule if yielding is required.
  - Returns `Poll::Ready` with the next iterator item or `Poll::Pending` to yield control.
- **Method `size_hint`**:
  - Delegates to the underlying iterator's `size_hint` for compatibility with stream combinators.

## Integration with the Project
- **Use Cases**:
  - Enables synchronous iterators (e.g., `vec![1,2,3].into_iter()`, ranges) to be used as asynchronous streams.
  - Forms the basis for stream combinators like `chain`, `peekable`, `skip_while`, and `take` (as seen in related context examples).
- **Cooperative Scheduling**:
  - The `yield_amt` logic ensures long-running iterators don't block the async runtime, aligning with Tokio's cooperative task model.

## Example Usage
```rust
let mut stream = stream::iter(vec![17, 19]);
assert_eq!(stream.next().await, Some(17)); // Asynchronous iteration
```

## Role in the Project