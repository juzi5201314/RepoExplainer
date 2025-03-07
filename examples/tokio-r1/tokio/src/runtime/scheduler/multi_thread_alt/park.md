# Tokio Runtime Scheduler Parking Mechanism

## Purpose
This file implements thread parking/unparking logic for Tokio's multi-threaded scheduler. It coordinates thread sleep/wake cycles using a combination of condition variables and driver-based event notification (I/O, timers), optimizing resource usage when threads are idle.

## Key Components

### Core Structures
- **`Parker`**: Main handle for parking operations (thread suspension)
- **`Unparker`**: Handle for waking parked threads
- **`Inner`**: Shared state container with:
  - Atomic state tracking (`EMPTY`, `PARKED*`, `NOTIFIED`)
  - Mutex/Condvar for synchronization
  - Shared driver access (I/O/timer resources)

### State Management
- **Atomic State Transitions**: Uses compare-and-swap operations for lock-free coordination:
  ```rust
  const EMPTY: usize = 0;
  const PARKED_CONDVAR: usize = 1;
  const PARKED_DRIVER: usize = 2;
  const NOTIFIED: usize = 3;
  ```

### Parking Strategies
1. **Driver-Based Parking**:
   - Uses Tokio's I/O/timer driver when available (`park_driver`)
   - Direct integration with OS-level event notification (epoll/kqueue)
   
2. **Condition Variable Fallback**:
   - Used when driver is busy (`park_condvar`)
   - Traditional thread blocking with mutex/condvar

### Critical Operations
- **`park()`**: Sequence:
  1. Check for immediate notification
  2. Attempt driver-based parking
  3. Fallback to condvar parking
- **`unpark()`**: 
  - Atomic state update to `NOTIFIED`
  - Driver wakeup or condvar notification
- **`shutdown()`**: 
  - Driver cleanup
  - Broadcast wakeup for all parked threads

## Integration with Tokio Runtime
- Coordinates with `driver::Handle` for I/O and timer operations
- Used by scheduler workers to pause when no tasks are available
- Enables efficient task wakeups through driver events
- Part of multi-thread scheduler's load balancing strategy

## Concurrency Considerations
- **Loom**-verified synchronization primitives
- Careful state transition ordering for memory safety
- Hybrid approach balances driver efficiency with condvar reliability
