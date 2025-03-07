# Tokio Runtime Configuration (`config.rs`)

## Purpose
This file defines the `Config` struct, which centralizes configuration parameters and callbacks for Tokio's runtime. It serves as a container for tuning scheduler behavior, task lifecycle hooks, metrics collection, and other runtime-specific settings.

## Key Components

### Core Configuration Fields
- **Task Scheduling**: 
  - `global_queue_interval`: Controls how often workers check the global task queue.
  - `local_queue_capacity`: Sets per-worker task queue size.
  - `disable_lifo_slot`: Disables LIFO task optimization (work-stealing preparation).

### Event Handling
- `event_interval`: Determines how frequently the runtime processes I/O/timer events.

### Lifecycle Hooks
- **Worker Threads**: `before_park`/`after_unpark` for thread parking events.
- **Task Hooks**: 
  - `before_spawn`/`after_termination` for task creation/destruction.
  - Unstable `before_poll`/`after_poll` (feature-gated) for poll monitoring.

### Advanced Features
- `seed_generator`: Enables deterministic RNG for reproducible task scheduling.
- `metrics_poll_count_histogram`: Configures runtime performance metrics collection.
- `unhandled_panic` (unstable): Defines panic handling strategy for tasks.

## Project Integration
- Used across scheduler implementations (multi-threaded/current-thread) via `runtime::Builder`.
- Accessed by components like:
  - Task queues and worker LIFO logic
  - Metrics subsystems
  - Runtime initialization flows
  - Panic handling mechanisms

## Conditional Compilation
- `#[cfg(tokio_unstable)]` gates experimental features like poll hooks.
- WASM targets and non-unstable builds exclude certain fields via `allow(dead_code)`.

---
