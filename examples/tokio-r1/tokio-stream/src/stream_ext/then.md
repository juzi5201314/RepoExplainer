# `then.rs` Module Explanation

## Purpose
Implements the `Then` stream combinator for asynchronous processing of stream elements through future transformations. Enables chaining asynchronous operations where each stream item is processed by a function returning a future.

## Key Components

### `Then` Struct
- **Fields**:
  - `stream`: Pinned source stream (type `St`)
  - `future`: Pinned optional future (type `Option<Fut>`) for tracking active async operation
  - `f`: Transformation function (type `F`) converting stream items to futures
- **Attributes**:
  - `#[must_use]` to enforce consumption through polling
  - `pin_project!` macro for safe pinning of fields

### Core Implementation
1. **Polling Logic** (`poll_next`):
   - Checks for active future first
   - Returns `Poll::Ready` when future completes
   - Processes next stream item when no active future
   - Propagates pending/termination states
2. **Size Hint**:
   - Combines source stream's size hint with pending future status
   - Maintains accurate lower/upper bound estimates

### Integration Points
- Implements `Stream` trait for interoperability
- Part of `StreamExt` extension methods (via `super::StreamExt::then`)
- Uses `pin_project_lite` for projection safety

## Relationship to Project
Works with other stream combinators (`fold`, `any`, `take_while`) in `tokio-stream` to provide:
- Asynchronous processing pipeline capabilities
- Chainable transformation operations
- Zero-cost abstractions for async stream processing

## Behavioral Characteristics
- Lazy evaluation: Only processes items when polled
- Backpressure-aware: Propagates pending states correctly
- Order-preserving: Maintains original stream order through sequential future execution
