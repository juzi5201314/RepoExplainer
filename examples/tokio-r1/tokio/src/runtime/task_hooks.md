# Tokio Task Hooks Implementation

## Purpose
This file implements task lifecycle hooks for Tokio's runtime, providing callback mechanisms for task-related events like spawning, termination, and polling. It enables instrumentation and monitoring of async tasks within the runtime.

## Key Components

### 1. `TaskHooks` Struct
- Central structure holding optional callbacks:
  - `task_spawn_callback`: Triggered when a task is spawned
  - `task_terminate_callback`: Triggered on task termination
  - Unstable polling hooks (`before_poll_callback`, `after_poll_callback`) under `tokio_unstable` flag

### 2. `TaskMeta` Struct
- Provides task metadata to callbacks:
  - Opaque `id` for task identification
  - PhantomData for lifetime management
- Unstable API with restricted visibility

### 3. Callback Handling
- `spawn()`: Invokes spawn callback with task metadata
- `poll_{start|stop}_callback()`: Unstable methods for poll phase instrumentation
- `from_config()`: Constructs hooks from runtime configuration

### 4. Type Definitions
- `TaskCallback`: Arc-wrapped callback function type with Send/Sync requirements

## Integration with Tokio
- Connects to runtime configuration through `Config` type
- Used in task spawning logic (`spawn()` calls)
- Integrates with unstable instrumentation features for detailed task observation
- Works with Tokio's cooperative scheduling through poll callbacks

## Key Relationships
- Part of Tokio's task module infrastructure
- Complements task spawning/management in `runtime::task`
- Enables user-defined instrumentation through callback registration
- Supports both stable and experimental features via conditional compilation
