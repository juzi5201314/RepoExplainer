# TaskTracker Module Explanation

## Purpose
The `TaskTracker` type provides a mechanism for tracking asynchronous tasks and waiting for their completion, particularly useful for implementing graceful shutdown patterns in Tokio applications. It coordinates with `CancellationToken` to signal shutdown while ensuring all tracked tasks complete before proceeding.

## Key Components

### 1. Core Structures
- **`TaskTracker`**: Main type holding an `Arc<TaskTrackerInner>` to share state.
- **`TaskTrackerInner`**: Internal state containing:
  - `state`: Atomic integer tracking task count (higher bits) and closed status (lowest bit).
  - `on_last_exit`: `Notify` primitive to signal when tasks are done.
- **`TaskTrackerToken`**: RAII guard representing a tracked task. Dropping it decrements the task count.
- **`TrackedFuture<F>`**: Wrapper around a future that automatically manages task tracking.
- **`TaskTrackerWaitFuture`**: Future returned by `wait()` that resolves when the tracker is closed and empty.

### 2. State Management
- **Atomic Operations**: Uses atomic bitwise operations to track task count and closed status efficiently.
- **Closed Flag**: The lowest bit of `state` indicates whether the tracker is closed.
- **Task Count**: The higher bits of `state` store the number of active tasks.

### 3. Key Methods
- **`spawn()`/`spawn_on()`**: Spawn tasks on Tokio runtimes while tracking them.
- **`close()`/`reopen()`**: Control whether the tracker allows `wait()` to complete.
- **`wait()`**: Returns a future that resolves when the tracker is closed and empty.
- **`track_future()`**: Wraps a future to automatically track its lifecycle.

### 4. Concurrency Handling
- Uses `Notify` to efficiently wake waiters when tasks complete.
- Implements ABA resistance in `wait()` to handle transient empty states.
- Atomic orderings (AcqRel/Release) ensure proper synchronization between task tracking and closure.

## Integration with Tokio
- Works alongside Tokio's `JoinHandle`, `LocalSet`, and runtime handles.
- Provides alternatives to `JoinSet` with lower memory overhead by not storing task results.
- Integrates with Tokio's spawning mechanisms for tasks, blocking operations, and local execution.

## Comparison to `JoinSet`
- **Advantages**:
  - Immediate memory reclamation when tasks exit.
  - Shared ownership via cloning.
  - Non-mutable task insertion.
  - Explicit control over shutdown signaling via `close()`.
- **Use Cases**: Preferred for long-running services requiring graceful shutdown or bulk task tracking without result collection.

## Example Flow
1. Create a `TaskTracker`.
2. Spawn tasks with `track_future()` or `spawn()`.
3. Signal shutdown via `close()` (often paired with `CancellationToken`).
4. Await completion with `wait()`.
5. All tasks complete before proceeding.

---
