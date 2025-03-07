# Tokio Current Thread Scheduler Implementation

## Overview
This file implements the `current_thread` scheduler for Tokio's runtime, designed for single-threaded task execution. It provides a lightweight executor that runs tasks on the current thread without worker threads, suitable for simple async applications or embedding Tokio in environments requiring strict single-threaded execution.

## Key Components

### 1. Core Structures
- **`CurrentThread`**: Main scheduler type containing:
  - `core`: Atomic reference to scheduler state (task queue, driver, metrics)
  - `notify`: Notification mechanism for cross-thread wakeups
- **`Handle`**: Shared reference to scheduler state with:
  - Task management components (owned tasks, injection queue)
  - Resource drivers (I/O, time)
  - Configuration and metrics
- **`Core`**: Transient scheduler state containing:
  - Local task queue
  - Runtime driver (I/O, timer)
  - Metrics collection
  - Scheduling configuration

### 2. Task Management
- **`OwnedTasks`**: Thread-safe collection tracking all spawned tasks
- **`Inject`**: Work-stealing queue for tasks spawned from other threads
- **`Defer`**: Mechanism for deferred task wakeups (e.g., yield_now)

### 3. Execution Flow
- **`block_on`**: Primary entry point that:
  1. Takes ownership of the scheduler core
  2. Sets up task context
  3. Runs the main future and processes tasks
  4. Implements cooperative scheduling with per-tick task processing
- **Task Processing**:
  - Checks local queue and global injection queue
  - Processes tasks in rounds (configurable via `event_interval`)
  - Integrates with runtime drivers for I/O and timer events

### 4. Shutdown Handling
- Drains all task queues
- Closes task collections
- Submits final metrics
- Shuts down resource drivers

## Important Features

### Metrics & Instrumentation
- Tracks scheduler metrics (task counts, queue depths)
- Supports Tokio's unstable metrics API
- Collects worker-specific statistics for monitoring

### Task Spawning
- Provides both thread-safe (`spawn`) and unsafe thread-local (`spawn_local`) variants
- Integrates with Tokio's task lifecycle hooks

### Specialized Functionality
- **Task Dumping**: Debugging support for capturing task traces (Linux-only)
- **Panic Handling**: Configurable shutdown behavior on unhandled task panics
- **Cooperative Scheduling**: Implements yield points and fairness through queue interval checks

## Integration with Tokio Runtime

### Relationship with Other Components
- Works with the global runtime context system
- Integrates with blocking task pool through `blocking_spawner`
- Shares common infrastructure with multi-thread scheduler:
  - Task management (OwnedTasks/Inject)
  - Driver interfaces
  - Metrics collection

### Thread-Local Management
Uses a thread-local `Context` to maintain:
- Scheduler handle reference
- Current core state
- Deferred wakeups

## Key Algorithms

### Scheduling Logic
1. Check global queue every N ticks (configurable via `global_queue_interval`)
2. Process local tasks first when possible
3. Yield to driver for I/O/timer events when queue is empty
4. Implement cooperative yielding through deferred wakeups

### Parking/Unparking
- Efficient thread parking using runtime driver integration
- Implements wakeup optimizations through atomic flags
- Supports configurable before_park/after_unpark hooks

## Safety Considerations
- Uses `loom` primitives for concurrency verification
- Carefully manages thread-local state transitions
- Implements proper shutdown sequencing to prevent resource leaks
