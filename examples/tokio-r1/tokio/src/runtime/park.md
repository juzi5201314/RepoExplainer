# Tokio Thread Parking Mechanism

## Purpose
This file implements the core thread parking/unparking mechanism for Tokio's runtime. It provides synchronization primitives to efficiently manage worker thread lifecycle (parking when idle, waking when work is available) and integrates with async task wakers.

## Key Components

### Core Structures
- `ParkThread`: Thread handle with parking capabilities
- `UnparkThread`: Handle to unpark a parked thread
- `Inner`: Shared state containing:
  - `state` atomic (EMPTY/PARKED/NOTIFIED)
  - `Mutex` and `Condvar` for synchronization
- `CachedParkThread`: Thread-local cached parker with waker integration

### State Management
Three atomic states coordinate thread parking:
- `EMPTY`: Initial state
- `PARKED`: Thread is parked/waiting
- `NOTIFIED`: Thread should wake up

### Parking Logic
- `park()`: 
  - Uses compare-and-swap to manage state transitions
  - Leverages condition variables with spurious wakeup protection
  - Implements fast path for immediate notifications
- `park_timeout()`: 
  - Similar to `park()` with duration limit
  - Special handling for WASM targets without atomics

### Unparking Mechanism
- `unpark()`: 
  - Atomic state transition to NOTIFIED
  - Condition variable notification
  - Handles synchronization through mutex locking

### Async Integration
- `into_waker()` converts `UnparkThread` to standard `Waker`
- `block_on()` runs futures using parking mechanism
- Raw waker vtable implementation bridges to unpark calls

### Loom Support
- Special thread-local counters for concurrency testing
- Atomic operations with SeqCst ordering for verification

## Project Integration
This implementation:
1. Forms the basis for worker thread management in Tokio's scheduler
2. Integrates with async task system through waker conversion
3. Provides timeout capabilities for runtime operations
4. Enables efficient resource usage via condition variable-based waiting
5. Supports both native and WASM targets (with fallbacks)

## Critical Details
- Uses compare-and-swap for atomic state management
- Handles spurious wakeups through state verification loops
- Maintains memory safety through proper atomic ordering (SeqCst)
- Implements thread-local caching via `tokio_thread_local!`
