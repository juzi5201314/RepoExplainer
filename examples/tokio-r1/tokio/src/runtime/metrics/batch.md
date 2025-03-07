# Tokio Runtime Metrics Batch Implementation

## Purpose
This file (`batch.rs`) implements a batching mechanism for collecting and submitting runtime metrics in Tokio's worker threads. It optimizes performance by aggregating metrics updates locally before flushing them to shared atomic counters, reducing contention on individual atomic operations.

## Key Components

### `MetricsBatch` Struct
- **Core Metrics Fields**: Tracks various worker thread activities:
  - Parking/unparking events (`park_count`, `park_unpark_count`)
  - Task polling statistics (`poll_count`, `noop_count`)
  - Work stealing metrics (`steal_count`, `steal_operations`)
  - Queue management (`overflow_count`, `local_schedule_count`)
  - Timing measurements (`busy_duration_total`, `processing_scheduled_tasks_started_at`)

### `PollTimer` Struct
- **Poll Timing Analysis**: Contains:
  - `poll_counts`: Histogram of task poll durations
  - `poll_started_at`: Timestamp for measuring individual poll times

### Critical Methods
1. **`new()`**: Initializes metrics with starting values and optional histogram tracking.
2. **`submit()`**: Flushes batched metrics to atomic counters in `WorkerMetrics`.
3. **Event Tracking Methods**:
   - `about_to_park()`/`unparked()`: Handle parking-related counters
   - `start_poll()`/`end_poll()`: Measure task polling durations
   - `incr_steal_count()`: Multi-thread specific work stealing metrics (gated by `cfg_rt_multi_thread!`)

### Optimization Features
- **Batched Atomic Updates**: Reduces atomic operation overhead by aggregating changes before submission
- **Histogram Support**: Optional detailed timing distribution tracking through `HistogramBatch`
- **Conditional Compilation**: Multi-thread specific metrics only included in appropriate runtime configurations

## Integration with Project
- Works with `WorkerMetrics` struct that provides atomic counters for runtime statistics
- Part of Tokio's metrics subsystem exposed through `RuntimeMetrics` API
- Used by worker threads to track performance characteristics without impacting scheduler performance

## Key Relationships
- **WorkerMetrics**: Receives final aggregated values through `submit()`
- **HistogramBatch**: Used for detailed timing distribution when enabled
- **Runtime Configuration**: `cfg_rt_multi_thread!` macro gates multi-processor specific metrics
