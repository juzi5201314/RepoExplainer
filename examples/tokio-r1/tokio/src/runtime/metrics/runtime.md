# Tokio Runtime Metrics Module

## Purpose
The `runtime.rs` file provides the `RuntimeMetrics` struct, which serves as a handle to access various runtime performance metrics in Tokio. It enables monitoring of internal runtime behavior, including task scheduling, worker thread activity, and resource utilization.

## Key Components

### Core Metrics
- **Worker Thread Count**: `num_workers()` returns configured worker threads
- **Alive Tasks**: `num_alive_tasks()` tracks active/in-progress tasks
- **Queue Depths**: `global_queue_depth()` and `worker_local_queue_depth()` show pending work

### Advanced Metrics (Unstable)
- **Blocking Threads**: `num_blocking_threads()` and `num_idle_blocking_threads()`
- **Worker-Specific Stats**: Parking counts, task stealing, poll counts per worker
- **Histograms**: Task poll time distributions (when enabled)
- **IO Driver Metrics**: File descriptor tracking and event counts

### Atomic Counters
Uses 64-bit atomic operations (`Relaxed` ordering) for:
- Task spawn counts
- Schedule counters
- Steal operations
- Parking statistics

## Important Features
1. **Worker Isolation**: Metrics per worker thread (index 0 to num_workers-1)
2. **Runtime Configuration Awareness**: Automatically handles current-thread vs multi-thread differences
3. **Deprecation Handling**: Maintains backwards compatibility for renamed metrics
4. **Conditional Metrics**: 
   - `cfg_unstable_metrics` gates experimental measurements
   - `cfg_64bit_metrics` enables high-resolution counters

## Integration Points
- Built on top of runtime `Handle` system
- Aggregates data from:
  - Scheduler metrics (global queue)
  - Worker thread metrics (per-worker stats)
  - Blocking thread pool
  - IO driver (when enabled)
- Interfaces with histogram infrastructure for time measurements

## Usage Patterns
Enables:
- Runtime health monitoring
- Workload balancing analysis
- Performance optimization
- Capacity planning
- Debugging task starvation/queue buildup

```markdown