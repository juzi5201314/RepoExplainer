# Tokio Multi-Thread Scheduler Handle

## Purpose
This file implements the `Handle` type for Tokio's alternative multi-threaded scheduler (`multi_thread_alt`). It serves as the primary interface for interacting with the scheduler, handling task spawning, shutdown coordination, and resource management.

## Key Components

### 1. Handle Structure
```rust
pub(crate) struct Handle {
    pub(super) shared: worker::Shared,
    pub(crate) driver: driver::Handle,
    pub(crate) blocking_spawner: blocking::Spawner,
    pub(crate) seed_generator: RngSeedGenerator,
    pub(crate) task_hooks: TaskHooks,
}
```
- **shared**: Shared state across worker threads
- **driver**: Manages I/O and timer resources
- **blocking_spawner**: Handles blocking task execution
- **seed_generator**: Provides RNG seeds for work-stealing
- **task_hooks**: Custom hooks for task lifecycle events

### 2. Core Functionality
- **Task Spawning** (`spawn`/`bind_new_task`):
  - Creates new tasks through worker-owned queues
  - Integrates with task lifecycle hooks
  - Automatically schedules spawned tasks
- **Shutdown Management**:
  - Triggers scheduler closure
  - Unparks driver to ensure proper resource cleanup

### 3. Special Features
- Conditional compilation for unstable metrics
- Task ID management for diagnostics
- Debug implementation that hides internal details

## Integration with Project
- Coordinates with worker threads through `worker::Shared`
- Interfaces with driver subsystem for I/O/timer management
- Uses Tokio's loom synchronization primitives for concurrency safety
- Part of the scheduler hierarchy (`multi_thread_alt` implementation)

## Conditional Features
- `cfg_unstable_metrics`: Enables metrics collection
- `cfg_unstable`: Exposes additional task identification capabilities
