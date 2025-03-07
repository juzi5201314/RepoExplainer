# Tokio I/O Driver Metrics Implementation

## Purpose
This file defines the `IoDriverMetrics` struct and its associated methods, which provide atomic counters for tracking I/O-related metrics in Tokio's runtime. These metrics monitor file descriptor (FD) lifecycle events and I/O readiness notifications.

## Key Components

### `IoDriverMetrics` Struct
- **Fields**:
  - `fd_registered_count`: Tracks total FDs registered with the I/O driver.
  - `fd_deregistered_count`: Tracks total FDs deregistered/removed.
  - `ready_count`: Counts I/O readiness events (e.g., socket readable/writable).

### Methods
1. **`incr_fd_count()`**  
   Increments FD registration counter (atomic add with `Relaxed` ordering).
2. **`dec_fd_count()`**  
   Increments FD deregistration counter.
3. **`incr_ready_count_by(amt: u64)`**  
   Accumulates readiness events in batches.

### Conditional Compilation
- Uses `#![cfg_attr(not(feature = "net"), allow(dead_code))]` to disable metrics when networking (`net` feature) is inactive.
- Part of a larger conditional compilation strategy for metrics collection (seen in related context).

## Integration with Project
- Used by Tokio's I/O driver to expose metrics through methods like `io_driver_fd_registered_count()`.
- Metrics are queried via `with_io_driver_metrics` pattern seen in related context.
- Integrates with Tokio's metrics system through `MetricAtomicU64` wrappers, which provide feature-gated metric collection.

## Performance Considerations
- Uses `Relaxed` memory ordering for atomic operations to minimize overhead, as exact operation ordering isn't critical for metric counters.

---
