# Timeout Module Explanation

## Purpose
This module implements timeout functionality for asynchronous operations in Tokio. It allows wrapping a future to execute with a maximum time limit, returning an error if the future doesn't complete within the specified duration or deadline.

## Key Components

### 1. Core Functions
- **`timeout(duration, future)`**:  
  Wraps a future to complete within `duration`. Returns `Result<T, Elapsed>`.
- **`timeout_at(deadline, future)`**:  
  Wraps a future to complete before an absolute `deadline`.

Both functions create a `Timeout` struct that combines the target future with a timer (`Sleep`).

### 2. Timeout Struct
```rust
pub struct Timeout<T> {
    value: T,    // Inner future
    delay: Sleep, // Timer tracking deadline
}
```
Implements `Future<Output = Result<T::Output, Elapsed>>`:
1. Polls the inner future first.
2. If not ready, checks the timer:
   - Returns `Ok(value)` if the inner future completes first.
   - Returns `Err(Elapsed)` if the timer expires first.

### 3. Cooperative Scheduling
Handles edge cases where the inner future exhausts Tokio's task budget:
- Uses `coop::has_budget_remaining()` to detect budget exhaustion.
- Polls the timer without budget constraints if the inner future drained the budget, preventing starvation.

### 4. Error Handling
- `Elapsed` error is returned when the timeout occurs.
- Clean cancellation via dropping the `Timeout` future.

## Integration with Tokio
- Relies on Tokio's time driver (`Sleep`) for efficient timer management.
- Works with Tokio's cooperative scheduling to ensure fair task execution.
- Used throughout Tokio's APIs (e.g., I/O operations, synchronization primitives) to add time limits.

## Examples
```rust
// Timeout after 10ms
let result = timeout(Duration::from_millis(10), async_task).await;

// Timeout at specific instant
let deadline = Instant::now() + Duration::from_secs(5);
let result = timeout_at(deadline, async_task).await;
```

## Panics & Safety
- Panics if used without a Tokio runtime timer enabled.
- Safe cancellation via drop semantics (no resource leaks).

---
