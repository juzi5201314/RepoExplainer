# Tokio Multi-Thread Scheduler Worker Implementation

## Purpose
This file implements the core logic for worker threads in Tokio's multi-threaded scheduler. It handles task execution, work stealing, blocking operations, and shutdown coordination across multiple threads.

## Key Components

### 1. Worker Architecture
- **Worker**: Manages per-thread state with:
  - `handle`: Reference to scheduler resources
  - `index`: Unique worker identifier
  - `core`: Atomic container for worker's core data
- **Core**: Contains thread-local execution state:
  - Local run queue and LIFO slot for task prioritization
  - Shutdown flags and synchronization primitives
  - Metrics collection and scheduling configuration

### 2. Task Scheduling
- **Work Stealing**: Implements cross-worker task stealing using:
  - Local queues with overflow to global inject queue
  - Randomized work stealing strategy to prevent contention
- **LIFO Optimization**: Prioritizes recently scheduled tasks for better cache locality
- **Task Execution**: Handles cooperative scheduling with budget tracking

### 3. Blocking Operations
- `block_in_place`: Handles blocking operations by:
  1. Moving core to new thread
  2. Preserving runtime context
  3. Maintaining scheduling fairness

### 4. Shutdown Process
- Multi-phase shutdown sequence:
  1. Close global queues
  2. Worker coordination through shared state
  3. Task cancellation and resource cleanup
  4. Final single-threaded cleanup phase

### 5. Metrics & Maintenance
- Per-worker statistics collection
- Regular maintenance tasks:
  - Queue balancing
  - Runtime configuration tuning
  - Trace status checks

## Integration with Project
- Coordinates with other scheduler components through:
  - Global inject queue (`inject::Shared`)
  - Shared worker state (`Shared` struct)
  - Driver integration for I/O and time management
- Implements critical path for task execution in multi-threaded runtime
- Works with Tokio's ownership system (`OwnedTasks`) for safe task management

## Key Algorithms
- Work stealing with backoff strategy
- LIFO slot management with fairness caps
- Cooperative scheduling with budget tracking
- Shutdown coordination using atomic state transitions

## Role in Project