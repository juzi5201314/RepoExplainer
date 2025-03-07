# Tokio Cooperative Task Budget Management

## Purpose
The `consume_budget.rs` file implements a mechanism for cooperative task scheduling in Tokio. Its primary purpose is to allow long-running computational tasks to voluntarily yield control back to the Tokio runtime when their allocated execution budget is exhausted, preventing task starvation and ensuring fair scheduling.

## Key Components

### `consume_budget()` Function
- **Async Yield Mechanism**: An async function that checks if a task's cooperative budget is exhausted
- **Poll-Based Check**: Uses `poll_fn` to create a future that:
  1. Tracks execution via `trace_leaf` for diagnostics (when tracing is enabled)
  2. Checks budget status using `poll_proceed` from Tokio's coop module
  3. Yields control via `Poll::Pending` if budget is exhausted
  4. Marks progress with `made_progress()` when resuming

### Cooperative Budget Management
- Integrates with Tokio's internal `coop` module
- Works with `poll_proceed` to track task execution budgets
- Maintains fairness without requiring I/O operations

## Implementation Details
- **Conditional Yielding**: Only yields when budget is fully exhausted
- **Tracing Integration**: Supports runtime diagnostics through `trace_leaf`
- **Lightweight Check**: Minimal overhead when budget remains available

## Usage Example
Enables cooperative behavior in CPU-bound async tasks:
```rust
async fn sum_iterator(input: &mut impl Iterator<Item=i64>) -> i64 {
    let mut sum = 0;
    while let Some(i) = input.next() {
        sum += i;
        tokio::task::consume_budget().await // Periodic budget check
    }
    sum
}
```

## Project Integration
- Part of Tokio's core task scheduling system
- Complements I/O-based yielding mechanisms
- Works with other coop components (`poll_proceed`, `budget`)
- Enables fair resource sharing across tasks
