# Tokio Runtime Parker Implementation

## Purpose
This file implements the parking/unparking mechanism for worker threads in Tokio's multi-threaded scheduler. It coordinates thread suspension (when idle) and wakeup (when work arrives) using a combination of condition variables and driver-based event notification.

## Key Components

### Core Structures
- **`Parker`**: Main handle for parking operations
  - Contains an `Inner` ARC for shared state
  - Manages driver access and notification state
- **`Unparker`**: Wakeup handle for parked threads
- **`Inner`**: Shared state between Parker/Unparker
  - Atomic state machine (`EMPTY`, `PARKED*`, `NOTIFIED`)
  - Mutex/Condvar for synchronization
  - Shared driver access for I/O/timer events

### State Management
- Atomic state transitions coordinate between:
  - Direct driver parking (for I/O/timer events)
  - Condition variable parking (fallback when driver is busy)
  - Notification tracking to avoid missed wakeups

### Parking Strategies
1. **Driver Parking** (Preferred):
   - Uses Tokio's I/O/timer driver via `park_driver()`
   - Efficient event-based wakeups using system notifications
2. **Condition Variable Parking** (Fallback):
   - Used when driver is locked by another thread
   - Traditional thread synchronization with `Condvar`

## Critical Operations
- **`park()`**: 
  - Attempts immediate return if already notified
  - Tries to acquire driver lock for efficient parking
  - Falls back to condvar parking if driver is busy
- **`unpark()`**:
  - Atomic state transition to NOTIFIED
  - Wakes appropriate mechanism (condvar or driver)
- **Shutdown Handling**:
  - Notifies all parked threads during termination
  - Cleans up driver resources

## Integration with Runtime
- Works with Tokio's driver system (I/O, timers)
- Coordinates with worker thread management in scheduler
- Part of the multi-threaded scheduler's idle management:
  - Worker threads park when task queues are empty
  - Unparking occurs when new tasks are scheduled or events fire

## Concurrency Considerations
- Uses loom for concurrency validation in tests
- Atomic ordering (SeqCst) ensures proper memory visibility
- State machine prevents race conditions between park/unpark
- TryLock pattern prevents thread contention on driver access

## Special Cases
- `park_timeout()` currently only supports zero-duration (used in loom tests)
- Separate handling for spurious wakeups in condvar path
- Shutdown sequence coordination between driver and condvar
