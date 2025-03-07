# skip.rs - Stream Skip Adapter Implementation

## Purpose
Implements the `skip` method for asynchronous streams, which filters out the first `N` elements from a stream before yielding subsequent values.

## Key Components

### Structs
- `Skip<St>`: Core adapter struct containing:
  - `stream: St`: Pinned inner stream being wrapped
  - `remaining: usize`: Counter for elements to skip

### Traits Implemented
1. **Debug**: Provides debug formatting while maintaining stream privacy
2. **Stream**: Core async stream implementation with:
   - `poll_next`: Main polling logic
   - `size_hint`: Size estimation adjustment

### Critical Methods
- `poll_next`:
  - Uses loop to discard elements until `remaining` reaches 0
  - Leverages `pin_project!` macro for safe pinned projections
  - Implements backpressure-aware polling pattern
- `size_hint`:
  - Adjusts inner stream's size estimates by subtracting skipped elements
  - Uses saturating subtraction to prevent underflow

## Implementation Details
- Uses `pin_project_lite` for safe pin projection patterns
- Maintains zero-cost abstraction principles common in async Rust
- Follows Tokio's stream adapter pattern seen in similar methods (`take`, `skip_while`)

## Project Context
Part of Tokio's stream extension methods (`StreamExt`), providing:
- Functional-style stream manipulation
- Compositional async processing capabilities
- Similar pattern to other adapters like `take_while` and `skip_while`
