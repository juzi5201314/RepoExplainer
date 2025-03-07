# Code File Explanation: `merge.rs`

## Purpose
This file implements the `Merge` stream combinator, which combines two input streams into a single output stream that interleaves items from both sources as they become available. It alternates polling order between the two streams to ensure fair handling.

## Key Components

### 1. `Merge` Struct
- **Fields**:
  - `a`, `b`: Fused streams (`Fuse<T>`, `Fuse<U>`) to safely handle terminated streams.
  - `a_first`: Boolean flag to toggle polling order between streams.
- **Pin Projection**: Uses `pin_project!` macro for safe pinned projections of stream fields.

### 2. Stream Implementation
- **poll_next()**:
  - Alternates polling order using `a_first` flag.
  - Calls helper `poll_next()` with reordered parameters based on toggle state.
  - Returns first available item from either stream, or `Pending`/termination state.
- **size_hint()**:
  - Combines size hints from both streams using `merge_size_hints` utility.

### 3. Helper Function
- **poll_next(first, second, cx)**:
  - Polls `first` stream, returns immediately if item available.
  - Polls `second` stream if first didn't produce.
  - Returns `Ready(None)` only when both streams are exhausted.
  - Maintains `done` flag to track completion state.

## Integration with Project
- Part of `StreamExt` extension trait methods (via `super::StreamExt::merge`).
- Uses `Fuse` wrapper from parent module to prevent polling terminated streams.
- Follows Tokio's stream combinator pattern using pin projections and poll-based execution.
- Complements other combinators like `chain`, `then`, and `take` shown in related context.

## Design Considerations
- **Fairness**: Alternating polling order prevents starvation of either stream.
- **Termination Handling**: Uses `Fuse` to safely continue polling after stream completion.
- **Efficiency**: Immediately returns items without buffering, preserving backpressure.

This file implements a stream merger that enables interleaved consumption of multiple asynchronous data sources in the Tokio ecosystem.  