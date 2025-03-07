# Tokio Cooperative Scheduling Module (`coop`)

## Purpose
This module implements cooperative scheduling utilities for Tokio's async runtime. It prevents task starvation by ensuring long-running tasks periodically yield control back to the executor, allowing other tasks to run.

## Key Components

### 1. Budget Tracking
- **`Budget` Struct**: Tracks remaining "work units" (initialized to 128) a task can perform before yielding.
  - `initial()`: Starts with default budget.
  - `unconstrained()`: Creates a budget with no limits.
  - `decrement()`: Reduces budget and checks exhaustion.

### 2. Cooperative Control Flow
- **`poll_proceed()`**: Core mechanism that:
  1. Checks current budget
  2. Decrements budget if available
  3. Returns `Poll::Pending` when budget exhausted
  4. Uses `RestoreOnPending` guard to reset budget if no progress made

### 3. Budget Management Utilities
- **`budget()`**: Executes code with default budget constraints.
- **`with_unconstrained()`**: Runs code without budget limitations.
- **`has_budget_remaining()`**: Checks if task has budget left (used in combinators/timeouts).

### 4. Future Wrapper
- **`Coop<F>`**: Wrapper future that integrates budget checking with any async operation:
  - Automatically checks budget before polling inner future
  - Tracks progress via `RestoreOnPending`

### 5. Thread-Local Storage Integration
- Uses Tokio's context system to store budget in thread-local storage.
- `context::budget()` accesses/modifies the current task's budget.

## Key Mechanisms
- **Yield Points**: Inserted through `coop::proceed().await` in async operations.
- **Budget Restoration**: Automatic budget reset via RAII guard (`RestoreOnPending`).
- **Unconstrained Mode**: Opt-out mechanism for special cases requiring uninterrupted execution.

## Integration with Tokio
- Used in Tokio's I/O primitives and combinators to prevent starvation.
- Integrates with runtime metrics (when enabled) to track forced yields.
- Works with both single-threaded and multi-threaded executors.

## Example Usage
```rust
// In a stream processor:
async fn process_stream(mut stream: impl Stream) {
    while let Some(item) = stream.next().await {
        tokio::coop::proceed().await; // Yield point
        process(item);
    }
}
```

## Testing
Comprehensive tests verify:
- Budget decrementing behavior
- Nested budget contexts
- Yield-on-exhaustion functionality
- Unconstrained mode operation

This module is essential for Tokio's fair task scheduling, ensuring efficient resource utilization while maintaining responsiveness in async applications.
