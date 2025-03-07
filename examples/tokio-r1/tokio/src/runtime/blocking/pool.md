# Tokio Blocking Thread Pool Implementation

## Purpose
This file implements a dedicated thread pool for executing blocking operations in Tokio's async runtime. It prevents long-running synchronous tasks from blocking the async executor threads, maintaining runtime efficiency.

## Key Components

### Core Structures
- **`BlockingPool`**: Main pool manager holding a `Spawner` and shutdown receiver.
- **`Spawner`**: Handles task scheduling and worker thread management (clonable via `Arc<Inner>`).
- **`Inner`**: Shared state containing:
  - Task queue (`VecDeque<Task>`)
  - Thread synchronization primitives (`Mutex`, `Condvar`)
  - Thread configuration (names, stack sizes)
  - Metrics tracking
- **`Task`**: Wrapper for blocking operations with mandatory/non-mandatory execution flags.

### Execution Flow
1. **Task Submission**:
   - `spawn_blocking` creates tasks marked as non-mandatory
   - `spawn_mandatory_blocking` creates tasks that must execute even during shutdown
2. **Thread Management**:
   - Workers wait on a condition variable with timeout
   - Dynamic thread scaling based on load (up to `thread_cap`)
   - Clean shutdown process with configurable timeout

### Metrics System
- Tracks:
  - Active/inactive thread counts
  - Queue depth (unstable feature)
- Atomic counters ensure lock-free metric updates

### Shutdown Handling
- Two-phase shutdown process:
  1. Signal shutdown to all workers
  2. Join worker threads with timeout
- Mandatory tasks complete during shutdown while non-mandatory get canceled

## Integration with Tokio
- Part of Tokio's runtime builder system
- Used by `Handle::spawn_blocking` API
- Integrates with runtime metrics system
- Works with Tokio's task system through `BlockingSchedule`

## Notable Features
- Mandatory task support for critical operations (e.g., filesystem sync)
- OS thread error recovery for temporary failures
- Loom testing support through ordered thread joining
- Stack size customization for worker threads
- Lifecycle hooks (`after_start`, `before_stop`)

## Critical Code Paths
- `Inner::run()` - Worker thread main loop
- `spawn_thread()` - OS thread creation
- `shutdown()` - Graceful termination logic
