# Tokio Multi-thread Scheduler Metrics Implementation

## Purpose
This file provides metric collection and monitoring capabilities for Tokio's multi-threaded scheduler. It implements various performance tracking methods on the scheduler's `Handle` structure, enabling observation of runtime behavior including task counts, queue depths, and worker thread statistics.

## Key Components

### Core Metrics
- `num_workers`: Returns active worker thread count
- `num_alive_tasks`: Tracks currently alive tasks
- `injection_queue_depth`: Measures global task queue size

### Unstable Metrics (Feature-gated)
```rust
cfg_unstable_metrics! {
    // Blocking thread statistics
    num_blocking_threads()
    num_idle_blocking_threads()
    
    // Detailed scheduler metrics
    scheduler_metrics() -> &SchedulerMetrics
    worker_metrics(usize) -> &WorkerMetrics
    
    // Queue depth tracking
    worker_local_queue_depth(usize) -> usize
    blocking_queue_depth() -> usize
    
    // 64-bit task counter (when enabled)
    cfg_64bit_metrics! { spawned_tasks_count() -> u64 }
}
```

## Implementation Details

### Conditional Compilation
- Uses Tokio's internal feature flags:
  - `cfg_unstable_metrics`: Gates advanced metrics collection
  - `cfg_64bit_metrics`: Enables 64-bit atomic counters

### Metric Sources
1. **Shared State**: Accesses worker metrics array and injection queue
2. **Blocking Spawner**: Tracks blocking thread pool statistics
3. **Scheduler Metrics**: Provides detailed runtime performance data
4. **Worker-specific Metrics**: Per-worker task queue information

## Integration with Project

### Relationship to Other Components
- Complements scheduler implementation in `multi_thread` module
- Integrates with worker thread management system
- Ties into Tokio's metrics subsystem through `SchedulerMetrics`/`WorkerMetrics`
- Works with blocking thread pool implementation

### Monitoring Capabilities
Enables collection of critical runtime statistics for:
- Task lifecycle tracking
- Queue congestion detection
- Thread pool utilization analysis
- Performance optimization decisions

## Role in Project