# Tokio Multi-thread Scheduler Metrics Implementation

## Purpose
This file provides metrics collection functionality for Tokio's multi-threaded scheduler, specifically tracking queue depths for task management. It enables monitoring of both the global injection queue and individual worker thread queues.

## Key Components

### Core Metrics Methods
1. **Injection Queue Depth**
   ```rust
   impl Shared {
       pub(crate) fn injection_queue_depth(&self) -> usize {
           self.inject.len()
       }
   }
   ```
   - Tracks number of tasks in the global injection queue
   - Used for monitoring cross-worker task distribution

2. **Worker Local Queue Depth (Conditional)**
   ```rust
   cfg_unstable_metrics! {
       impl Shared {
           pub(crate) fn worker_local_queue_depth(&self, worker: usize) -> usize {
               self.remotes[worker].steal.len()
           }
       }
   }
   ```
   - Conditionally compiled behind `cfg_unstable_metrics` flag
   - Measures task count in specific worker's steal queue
   - Essential for load balancing insights

## Implementation Details

### Conditional Compilation
- Uses `cfg_unstable_metrics!` macro to gate advanced metrics
- Allows gradual rollout of metrics features
- Maintains stable API surface by default

### Architectural Integration
- Works with `Shared` struct that manages scheduler state
- Integrates with worker stealing mechanism (`remotes[worker].steal`)
- Complements other metrics components (`WorkerMetrics`, `SchedulerMetrics`)

## Relationship to Overall Project
- Part of Tokio's runtime metrics system
- Provides low-level data for performance analysis
- Enables dynamic tuning of worker threads
- Supports debugging of task scheduling issues
