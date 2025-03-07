# Tokio `select!` Macro Implementation

## Purpose
This file implements the `select!` macro, a core concurrency primitive in Tokio that allows waiting on multiple asynchronous branches simultaneously. It returns when the **first** branch completes, canceling all remaining branches. This enables efficient coordination between concurrent tasks within a single thread.

## Key Components

### Macro Structure
1. **Documentation Generation** (`doc!` macro):
   - Provides extensive usage examples, fairness considerations, cancellation safety details, and ecosystem alternatives.
   - Explains branch patterns (`<pattern> = <async expr> => <handler>`), `else` branches, and precondition guards (`if` clauses).

2. **Core Implementation**:
   - Uses recursive macro rules to normalize input branches and generate polling logic.
   - Handles two modes:
     - **Unbiased** (default): Randomizes polling order for fairness.
     - **Biased**: Processes branches top-to-bottom (enabled via `biased;` keyword).

3. **Polling Mechanism**:
   - Aggregates futures into a tuple and polls them concurrently using `poll_fn`.
   - Tracks disabled branches via bitmask (`disabled: Mask`) based on preconditions/pattern mismatches.
   - Returns `Ready` when the first future completes successfully.

4. **Helper Macros**:
   - `count!`: Counts branches using token munching.
   - `count_field!`: Accesses tuple fields positionally.
   - `select_variant!`: Generates enum variants for branch results.

### Key Features
- **Cancellation Safety**: Automatically drops uncompleted futures when a branch finishes.
- **Pattern Matching**: Validates completed future results against user-specified patterns.
- **Else Handling**: Executes fallback code when all branches are disabled.
- **Thread-Local Concurrency**: Futures run on the current task without parallelism.

## Integration with Tokio
- Part of Tokio's macro API (`tokio::macros`).
- Works with Tokio's runtime to enable single-threaded concurrency.
- Complements other concurrency primitives like `join!` (wait for all) and `try_join!` (error-early).

## Example Flow
```rust
tokio::select! {
    _ = async_op1() => handle1,
    data = async_op2() if precondition => handle2,
    else => fallback,
}
```
1. Evaluate preconditions, disable non-eligible branches.
2. Poll active futures in order (biased) or random (unbiased).
3. Match first completed future's result against pattern.
4. Execute handler or fallback.

## Safety Considerations
- **Unpin Requirement**: Futures must be `Unpin` when reused across `select!` calls.
- **Cancellation Risks**: Documents cancellation-safe vs unsafe APIs (e.g., `recv` vs `write_all`).
- **Pattern Guarding**: Prevents accidental acceptance of mismatched results.
