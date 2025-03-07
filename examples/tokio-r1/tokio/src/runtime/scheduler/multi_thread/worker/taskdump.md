# Tokio Task Dump Implementation

## Purpose
This file implements task tracing and dumping functionality for Tokio's multi-threaded scheduler. It enables capturing snapshots of all active tasks across worker threads for debugging and monitoring purposes.

## Key Components

### Handle::trace_core
1. **Coordination**: Uses a double barrier system with timeout to:
   - Ensure only one worker (leader) performs tracing
   - Prevent partial traces during concurrent attempts
   - Allow graceful timeout (250ms) if coordination fails

2. **Task Collection**:
   - Steals tasks from all worker threads into a local queue
   - Uses unsafe `trace_multi_thread` to safely access shared task queues
   - Converts raw traces into structured `dump::Task` objects

3. **Result Handling**:
   - Stores collected traces in shared `trace_status`
   - Releases other workers via barrier synchronization

### Shared::steal_all
- Aggregates tasks from all remote worker queues
- Uses per-worker stealing mechanism to collect pending tasks
- Maintains statistics through `Stats` tracking

## Implementation Details
- **Concurrency Control**: Uses `loom` synchronization primitives for correct async behavior
- **Safety**: Unsafe block justified by controlled access to shared scheduler state
- **Metrics Integration**: Collects worker statistics during stealing operations
- **Feature Gating**: Conditional compilation (`cfg_taskdump`) enables tracing support

## Project Integration
- Works with task system through `OwnedTasks` and injection queue
- Integrates with runtime diagnostics via `dump::Dump` structure
- Complements single-threaded tracing in `current_thread` scheduler
- Part of Tokio's runtime observability infrastructure
