# Tokio `JoinSet` Implementation

## Purpose
The `join_set.rs` file implements the `JoinSet` type, a utility for managing and awaiting multiple asynchronous tasks in Tokio. It allows grouping spawned tasks, tracking their completion, and retrieving results in the order they finish. This is particularly useful for scenarios requiring concurrent task execution with non-deterministic completion order.

## Key Components

### `JoinSet<T>` Struct
- **Core Structure**: Wraps an `IdleNotifiedSet<JoinHandle<T>>` to manage spawned tasks efficiently.
- **Task Management**: Maintains a collection of tasks while providing methods to spawn, abort, and await their results.

### Main Features
1. **Task Spawning**:
   - Multiple variants (`spawn`, `spawn_on`, `spawn_local`, `spawn_blocking`) for different execution contexts.
   - Returns `AbortHandle` for remote cancellation.
   - Integrates with Tokio's runtime, `LocalSet`, and blocking threadpool.

2. **Result Retrieval**:
   - `join_next()`: Async method yielding completed task results.
   - `try_join_next()`: Non-blocking check for immediate results.
   - `join_all()`: Convenience method to collect all results into a vector.

3. **Lifecycle Management**:
   - `abort_all()`: Immediately cancels all tasks.
   - `shutdown()`: Graceful termination (aborts + awaits completion).
   - Automatic abort-on-drop behavior prevents resource leaks.

4. **Task Configuration**:
   - `Builder` type (unstable feature) for pre-spawn configuration like task naming via tracing.

### Internal Mechanics
- **IdleNotifiedSet**: Underlying data structure managing task states (idle/notified) for efficient polling.
- **Waker Integration**: Properly handles task wakeups using runtime context.
- **Cooperative Scheduling**: Respects Tokio's coop budget to prevent task starvation.

## Integration with Tokio
- Works with core Tokio components (`Handle`, `LocalSet`, blocking pool).
- Complements other task utilities like `JoinHandle` and `AbortHandle`.
- Designed for use in async contexts (requires Tokio runtime).

## Example Usage
```rust
let mut set = JoinSet::new();
set.spawn(async { 1 });
set.spawn_blocking(|| heavy_computation());
while let Some(res) = set.join_next().await {
    // Handle results
}
```

## Role in Project