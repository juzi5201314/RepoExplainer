# Tokio Runtime Context Management

## Purpose
This file manages thread-local runtime context information for Tokio's asynchronous runtime. It maintains critical state about task execution environments, scheduler interactions, and runtime configuration on a per-thread basis.

## Key Components

### Context Struct
The core `Context` struct contains:
- **Thread Identification**: `thread_id` for unique thread tracking
- **Scheduler State**: `current` and `scheduler` handles for runtime operations
- **Task Management**: `current_task_id` for tracking active tasks
- **Runtime Tracking**: `runtime` cell for enter/exit state management
- **Utilities**: Random number generator (`rng`) and cooperative budgeting system
- **Debugging**: Task tracing support for diagnostics

### Thread-Local Storage
The `tokio_thread_local!` macro creates a `CONTEXT` thread-local variable that stores the runtime context, ensuring isolation between threads while allowing efficient access to runtime state.

### Critical Functionality
1. **Cooperative Scheduling**:
   - `budget()` manages task yield behavior through cooperative budgeting
   - `defer()` handles task wakeup strategies

2. **Runtime Management**:
   - `set_scheduler()`/`with_scheduler()` for scheduler context switching
   - `enter_runtime` tracking for nested runtime entries

3. **Task Operations**:
   - Current task ID management with `set_current_task_id()`
   - Tracing support for task debugging (conditional compilation)

4. **Utilities**:
   - Thread-local random number generation (`thread_rng_n()`)
   - Thread ID management (`thread_id()`)

## Integration with Project
This file acts as the central hub for thread-specific runtime state management:
- Coordinates with scheduler implementations (multi-threaded/single-threaded)
- Supports task execution through cooperative budgeting
- Enables cross-cutting concerns like random number generation
- Provides foundation for runtime features (blocking operations, task dumps)

## Conditional Compilation
Extensive use of feature flags (`cfg_rt!`, `cfg_rt_multi_thread!`) allows:
- Selective inclusion of runtime components
- Support for different runtime configurations
- Conditional debugging/tracing features

## Safety Considerations
- Uses `loom` primitives for thread-safe access checking
- Manages unsafe operations through careful scoping
- Implements runtime entry/exit guards for state consistency
