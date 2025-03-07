# tokio/src/macros/try_join.rs

## Purpose
This file implements the `try_join!` macro for Tokio, enabling concurrent execution of multiple async operations that return `Result` values. It returns either:
- An aggregated `Ok` containing all successful results when **all** branches succeed
- An immediate `Err` when **any** branch fails early

## Key Components

### Documentation Macro (`doc!`)
- Generates comprehensive docs explaining behavior, runtime characteristics, and usage examples
- Highlights differences from `join!` macro (error handling vs success-only aggregation)
- Warns about concurrent-but-not-parallel execution model

### Macro Implementation
1. **Conditional Compilation**:
   - Simplified version for documentation generation (`#[cfg(doc)]`)
   - Full implementation for runtime use (`#[cfg(not(doc))]`)

2. Core Logic:
   - Creates pinned futures using `maybe_done`
   - Implements round-robin polling with `skip_next_time` counter
   - Short-circuits on first error using pattern:
     ```rust
     if fut.as_mut().output_mut().expect(...).is_err() {
         return Ready(Err(...))
     }
     ```
   - Aggregates successful results using tuple destructuring

3. Safety Mechanisms:
   - Uses `Pin::new_unchecked` with stack-pinned futures
   - Implements poll rotation to prevent starvation

## Integration with Tokio
- Complements `join!` macro with error handling capabilities
- Works with Tokio's task system through `tokio::spawn` integration
- Part of Tokio's macro utilities for async control flow
- Leverages internal types like `maybe_done` and `poll_fn`

## Runtime Characteristics
- Concurrent execution on same task (no parallelism)
- Zero-allocation design
- Fair polling through index rotation
- Early termination on first error
