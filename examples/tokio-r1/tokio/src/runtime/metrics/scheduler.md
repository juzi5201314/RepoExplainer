# Tokio Scheduler Metrics Module

## Purpose
This file defines the `SchedulerMetrics` struct responsible for tracking key scheduler-related metrics in Tokio's runtime. It focuses on monitoring task scheduling patterns and cooperative task yielding behavior.

## Key Components

### Core Struct
- **`SchedulerMetrics`**: Tracks two critical metrics using atomic counters:
  - `remote_schedule_count`: Counts tasks scheduled from outside the runtime (cross-thread scheduling)
  - `budget_forced_yield_count`: Counts tasks forced to yield due to exhausted execution budgets

### Atomic Operations
- Uses `MetricAtomicU64` wrapper for thread-safe metric tracking
- Implements atomic increments with `Relaxed` ordering for low-overhead updates

### Methods
- `new()`: Initializes metric counters to zero
- `inc_remote_schedule_count()`: Increments external task scheduling counter
- `inc_budget_forced_yield_count()`: Increments budget enforcement counter

## Integration with Runtime
- Part of Tokio's unstable metrics API (requires feature flag)
- Accessed through runtime components via `scheduler_metrics()` getter
- Complements `WorkerMetrics` which tracks per-worker statistics
- Used in cooperative scheduling system to monitor task execution fairness

## Relationship to Other Components
- Works with worker threads' local metrics (`local_schedule_count`)
- Tied to task injection systems (`Inject`/`Overflow` mechanisms)
- Integrated with runtime statistics collection for performance analysis

This file provides essential metrics infrastructure for monitoring and optimizing Tokio's task scheduler behavior.  