# Tokio Blocking Scheduler Explanation

## Purpose
This file (`schedule.rs`) implements a custom task scheduler for **blocking operations** in the Tokio runtime. It provides specialized handling for blocking tasks (non-async I/O) to prevent them from interfering with the main async task scheduler.

## Key Components

### `BlockingSchedule` Struct
- Core type implementing `task::Schedule` trait for blocking tasks
- Contains:
  - `handle`: Runtime handle (test-util only)
  - `hooks`: Task lifecycle callbacks (particularly termination hooks)

### Critical Methods
1. **`new()` Constructor**
   - Initializes scheduler with runtime handle
   - Test-util feature: Inhibits auto-time-advancing for CurrentThread scheduler
   - Clones task termination hooks from runtime configuration

2. **`release()` Implementation**
   - Test-util: Re-enables time auto-advancement and unparks driver
   - Returns `None` as blocking tasks aren't recycled

3. **`schedule()` Method**
   - Panics (`unreachable!()`) since blocking tasks shouldn't be rescheduled

4. **`hooks()` Accessor**
   - Provides cloned task termination callback for proper lifecycle management

## Test Utilities
- Conditional compilation (`cfg(feature = "test-util")`) enables:
  - Time manipulation for deterministic testing
  - Driver unparking to simulate task completion
  - Special handling for different scheduler types

## Integration with Tokio
- Works with blocking task pool to isolate CPU-bound operations
- Maintains runtime hooks for proper task lifecycle tracking
- Complements async schedulers by offloading blocking operations
- Enables hybrid async/blocking execution without starving async tasks
