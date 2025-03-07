# Tokio Scheduler Module Explanation

## Purpose
This module serves as the core scheduler implementation for Tokio's runtime, providing abstractions for both single-threaded (`current_thread`) and multi-threaded (`multi_thread`) execution models. It handles task scheduling, worker thread management, and runtime configuration through feature flags.

## Key Components

### 1. Conditional Compilation
- Uses `cfg_rt!`/`cfg_rt_multi_thread!` macros to enable runtime features based on compilation flags
- Supports three scheduler variants:
  - `CurrentThread`: Single-threaded executor
  - `MultiThread`: Work-stealing multi-threaded scheduler
  - `MultiThreadAlt`: Experimental alternative implementation (unstable)

### 2. Core Structures
**`Handle` Enum**:
- Represents different scheduler instances with thread-safe references (`Arc`)
- Methods provide unified interface for:
  - Task spawning (`spawn`, `spawn_local`)
  - Runtime shutdown
  - Metrics collection
  - Driver access (I/O, time)

**`Context` Enum**:
- Tracks execution context for different scheduler types
- Handles task deferral and worker thread management

### 3. Critical Functionality
- **Task Management**:
  - `spawn()` creates new tasks with proper scheduling
  - `spawn_local()` for thread-local tasks (current thread only)
- **Runtime Control**:
  - `shutdown()` initiates graceful termination
  - `blocking_spawner()` manages blocking operations
- **Thread Safety**:
  - `is_local()` checks if in single-threaded context
  - `can_spawn_local_on_local_runtime()` verifies thread ownership

### 4. Advanced Features
- **Metrics Collection** (unstable):
  - Tracks spawned tasks, worker queue depths, blocking operations
  - Provides scheduler/worker metrics through `unstable_metrics` feature
- **Seed Generation**:
  - `RngSeedGenerator` for deterministic random number generation
- **Hooks System**:
  - `TaskHooks` for custom task lifecycle handling

## Integration with Project
- Coordinates with other runtime components:
  - **Driver**: Handles I/O and timer resources
  - **Blocking Pool**: Manages CPU-bound operations
  - **Task System**: Implements future execution
- Acts as bridge between public API (`Runtime`) and low-level scheduling details
- Enables feature-flag based selection of execution model:
  - `rt` for basic runtime
  - `rt-multi-thread` for work-stealing scheduler

## Conditional Implementation
```rust
cfg_rt! { /* single-threaded components */ }
cfg_rt_multi_thread! { /* multi-threaded components */ }
cfg_unstable! { /* experimental features */ }
```
