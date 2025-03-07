# Tokio Interval Module Explanation

## Purpose
This module implements an `Interval` type for periodic task scheduling in asynchronous Rust applications using Tokio. It provides configurable strategies for handling missed ticks and integrates with Tokio's time utilities.

## Key Components

### 1. Interval Creation
- **`interval()`**: Creates an interval starting immediately with given duration
- **`interval_at()`**: Creates an interval starting at a specific `Instant`
- Both panic if period is zero and use internal tracing when enabled

### 2. Interval Structure
```rust
pub struct Interval {
    delay: Pin<Box<Sleep>>,          // Underlying sleep future
    period: Duration,                // Fixed interval duration
    missed_tick_behavior: MissedTickBehavior, // Handling strategy
    #[cfg(tracing)] resource_span: tracing::Span
}
```

### 3. Missed Tick Handling
`MissedTickBehavior` enum defines three strategies:
- **`Burst`**: Catch up immediately (default)
- **`Delay`**: Continue from current time
- **`Skip`**: Align to next period multiple

### 4. Core Functionality
- **`tick().await`**: Async method yielding at each interval
- **`poll_tick()`**: Core polling logic handling schedule adjustments
- Multiple reset methods (`reset()`, `reset_at()`, etc.) for schedule control

## Behavioral Characteristics
- First tick completes immediately by default
- Maintains periodic execution even with delayed ticks
- Provides cancellation safety for use in async select! statements
- Integrates with Tokio's time system for efficient wakeups

## Integration with Project
- Foundational component of Tokio's time module
- Used by higher-level timing utilities and stream wrappers
- Enables periodic task execution in async workflows
- Works with Tokio's tracing infrastructure when enabled

## Example Usage
```rust
let mut interval = interval(Duration::from_secs(1));
loop {
    interval.tick().await;
    periodic_task();
}
```
