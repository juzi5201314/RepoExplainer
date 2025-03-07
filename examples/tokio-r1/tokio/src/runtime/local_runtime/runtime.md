# Tokio Local Runtime (`runtime.rs`) Explanation

## Purpose
This file implements `LocalRuntime`, a single-threaded Tokio runtime designed to execute non-`Send`/non-`Sync` futures without requiring a `LocalSet`. It provides a lightweight execution environment optimized for:
- Local task spawning (`spawn_local`)
- Current-thread task scheduling
- Blocking operation management
- Context-aware async operations

## Key Components

### 1. Core Structure
```rust
pub struct LocalRuntime {
    scheduler: LocalRuntimeScheduler, // Current-thread scheduler
    handle: Handle,                   // Runtime control handle
    blocking_pool: BlockingPool,      // Dedicated blocking operations pool
    _phantom: PhantomData<*mut u8>,   // Enforce !Send/!Sync
}
```

### 2. Scheduler Implementation
```rust
pub(crate) enum LocalRuntimeScheduler {
    CurrentThread(CurrentThread)  // Single-threaded executor
}
```

### 3. Critical Methods
- **`new()`**: Initializes runtime with default current-thread configuration
- **`spawn_local()`**: Spawns non-`Send` futures directly onto local task queue
- **`block_on()`**: Executes future to completion (runtime entry point)
- **`shutdown_timeout()`**: Graceful shutdown with timeout
- **`enter()`**: Establishes runtime context for nested async operations

## Key Features

### Task Management
- Specialized `spawn_local` for non-`Send` futures
- Automatic future boxing based on size threshold (`BOX_FUTURE_THRESHOLD`)
- Integrated blocking task pool (`spawn_blocking`)

### Execution Control
- Current-thread scheduler guarantees task locality
- Thread-local context management
- Integrated instrumentation for:
  - Task tracing (unstable feature)
  - Runtime metrics collection

### Safety Mechanisms
- `PhantomData` ensures !Send/!Sync semantics
- Guarded context entry/exit
- Atomic shutdown coordination

## Integration with Tokio Ecosystem

1. **Scheduler Coordination**
   - Leverages `CurrentThread` scheduler from Tokio core
   - Integrates with blocking operation subsystem

2. **Handle System**
   - Provides `Handle` for cross-context operations
   - Enables spawner access across thread boundaries

3. **Instrumentation**
   - Works with tracing subsystem
   - Supports task dumps (Linux-specific)

## Usage Patterns

### Basic Initialization
```rust
let rt = LocalRuntime::new().unwrap();
rt.block_on(async {
    // Async work here
});
```

### Context Management
```rust
let guard = rt.enter();
// Context-aware operations
```

### Task Spawning
```rust
rt.spawn_local(async { /* Non-Send work */ });
rt.spawn_blocking(|| { /* CPU-intensive work */ });
```

## Safety Considerations
- Strict !Send/!Sync enforcement through type system
- Context-aware drop implementation
- Guarded memory management for futures
- Thread-local resource cleanup

---
