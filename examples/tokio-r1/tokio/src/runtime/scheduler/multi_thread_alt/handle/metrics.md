# Metrics Handling in Tokio's Multi-Threaded Scheduler

## Purpose
This file implements metrics collection for Tokio's alternate multi-threaded scheduler (`multi_thread_alt`). It provides runtime statistics about worker threads, task queues, blocking operations, and scheduler performance.

## Key Components

### Worker Metrics
- `num_workers()`: Returns total worker threads via `worker_metrics` length
- `worker_metrics(worker)`: Accesses per-worker metrics (queue depth, etc.)
- `worker_local_queue_depth()`: Gets depth of a specific worker's local task queue

### Blocking Thread Metrics
- `num_blocking_threads()`: Calculates dedicated blocking threads (total - workers)
- `num_idle_blocking_threads()`: Exposes idle threads in blocking thread pool
- `blocking_queue_depth()`: Shows pending blocking tasks in queue

### Task Metrics
- `num_alive_tasks()`: Counts currently active tasks
- `spawned_tasks_count()`: Tracks total spawned tasks (64-bit only)
- `injection_queue_depth()`: Measures global task queue depth

### Scheduler Metrics
- `scheduler_metrics()`: Provides access to scheduler-level statistics

## Implementation Details
- Uses atomic counters for thread-safe metric updates
- Handles 32/64-bit differences via `cfg_64bit_metrics!` macro
- Integrates with Tokio's metric atomics system
- Separates worker metrics from blocking pool metrics

## Project Integration
- Part of runtime monitoring system
- Used for performance analysis and debugging
- Informs scheduler decisions (work stealing, thread scaling)
- Integrates with Tokio's unstable metrics API
- Supports both stable and experimental metric collection
