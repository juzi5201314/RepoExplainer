# Tokio Scheduler Statistics Module Explanation

## Purpose
This module (`stats.rs`) is responsible for collecting runtime statistics and tuning the Tokio multi-threaded scheduler's performance parameters. It handles metrics tracking, adaptive scheduling optimization, and transient state management during task processing.

## Key Components

### 1. Core Structures
- **`Stats`**: Persistent statistics container with:
  - `MetricsBatch`: Aggregates runtime metrics for reporting
  - `task_poll_time_ewma`: Exponentially Weighted Moving Average of task polling times
- **`Ephemeral`**: Transient state for batch processing:
  - Timing information
  - Task count tracking
  - Debug validation flags

### 2. Adaptive Scheduling Logic
- **Global Queue Interval Tuning**:
  - Dynamically adjusts how many tasks are polled before checking the global queue
  - Uses EWMA of task poll times to balance local vs global queue processing
  - Default target: 61 tasks per interval (μs granularity)
  - Implements safety bounds (2-127 tasks)

### 3. Metrics Management
- **Time Tracking**:
  - Measures batch processing durations
  - Calculates average task poll times
- **Counters**:
  - Tracks tasks polled, steals, overflows
  - Maintains schedule counts
- **EWMA Calculations**:
  - Weighted average updates using `TASK_POLL_TIME_EWMA_ALPHA` (0.1)
  - Batch-weighted alpha adjustment for stability

### 4. Debug Features
- Validation of batch processing state transitions
- Debug assertions for proper start/end pairing

## Integration Points
- Interfaces with `WorkerMetrics` for metric reporting
- Consumes `Config` for user-defined settings
- Collaborates with scheduler components through:
  - Task polling lifecycle hooks
  - Parking/unparking notifications
  - Steal operation tracking

## Critical Methods
- `tuned_global_queue_interval()`: Core adaptive algorithm
- `end_processing_scheduled_tasks()`: EWMA update logic
- Metric submission pipeline to `WorkerMetrics`

## Performance Considerations
- Avoids atomic operations through batched metrics
- Uses nanoseconds precision for timing
- Saturating casts for numerical safety
- Conditional debug checks (compile-time eliminated)
