# Tokio Multi-Thread Scheduler Statistics Module

## Purpose
This module manages per-worker thread statistics for Tokio's multi-threaded scheduler. It handles:
1. Runtime metric collection and reporting
2. Adaptive scheduler tuning using exponential moving averages
3. Task polling performance tracking
4. Global queue interval optimization

## Key Components

### Core Structures
- `Stats`: Main statistics container tracking:
  - Metrics batch for user-facing statistics
  - Timing of task processing batches
  - Task polling counts
  - Exponential Weighted Moving Average (EWMA) of task poll times

### Important Constants
- `TASK_POLL_TIME_EWMA_ALPHA`: Smoothing factor for poll time averages (0.1)
- `TARGET_GLOBAL_QUEUE_INTERVAL`: Ideal 200μs interval for global queue checks
- Clamping values for global queue interval tuning (2-127 tasks)

### Critical Methods
1. **Dynamic Queue Tuning** (`tuned_global_queue_interval`):
   - Adjusts global queue check frequency based on current EWMA
   - Maintains balance between local and global task processing
   - Respects manual configuration overrides

2. **Batch Processing Tracking**:
   - `start/end_processing_scheduled_tasks` manages batch timing
   - Updates EWMA using weighted averages based on actual performance

3. **Metric Collection**:
   - Tracks parking/unparking events
   - Monitors task polls, steals, and overflows
   - Submits aggregated metrics to worker metrics

## Adaptive Scheduling
Uses exponential moving averages to:
- Calculate mean task poll duration per batch
- Adjust scheduler behavior based on recent performance
- Automatically tune global queue check frequency
- Maintain stability through value clamping

## Integration with Runtime
- Works with `WorkerMetrics` for metric reporting
- Consumes `Config` for manual tuning overrides
- Collaborates with scheduler components through metric batches
- Forms part of Tokio's observability infrastructure
