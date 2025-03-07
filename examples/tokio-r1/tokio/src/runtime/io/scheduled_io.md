# Tokio Runtime IO Scheduler (`scheduled_io.rs`)

## Purpose
This file implements the core synchronization mechanism for asynchronous I/O operations in Tokio's runtime. It manages readiness tracking and task wakeups for I/O resources like sockets, enabling efficient polling and notification when I/O operations can be performed.

## Key Components

### 1. `ScheduledIo` Struct
- **Core Data Structure**: Represents an I/O resource's state in the driver's slab.
- **Fields**:
  - `readiness`: Atomic value tracking readiness state, driver tick, and shutdown status using bit packing
  - `waiters`: Mutex-protected wait lists and dedicated reader/writer wakers
  - Cache-padded alignment to prevent false sharing across architectures

### 2. Readiness Tracking
- **Bit-packed AtomicUsize**:
  - 1 bit for shutdown status
  - 15 bits for driver tick (epoch counter)
  - 16 bits for readiness flags (using `Ready` bitmask)
- **Operations**:
  - `set_readiness`: Updates state with tick validation
  - `clear_readiness`: Resets readiness while preserving closed states

### 3. Wait Management
- **Waiters Structure**:
  - `list`: Linked list of general waiters
  - Dedicated `reader` and `writer` wakers for common cases
- **Waiter Node**:
  - Contains interest mask (read/write), waker, and ready flag
  - Managed through intrusive linked list

### 4. Synchronization Primitives
- `WakeList` for batch wakeup of tasks
- Locking strategy that releases mutex before notifying to prevent deadlocks
- Architecture-specific cache alignment to prevent false sharing

### 5. Async Interface
- `Readiness` future:
  - Manages state transitions (Init → Waiting → Done)
  - Integrates with Tokio's async task system through waker registration
  - Implements efficient polling with lock contention reduction

## Integration with Runtime
- Part of Tokio's I/O driver system
- Works with:
  - OS-level event notification (e.g., epoll, kqueue)
  - Task scheduling through waker system
  - Resource management via driver slab allocation
- Enables `AsyncRead`/`AsyncWrite` implementations through `poll_readiness`

## Critical Operations
1. **Event Notification**:
   - `wake()` processes waiters when readiness changes
   - Batches wakeups using `WakeList` for efficiency
2. **State Management**:
   - Atomic updates with tick validation prevent stale events
   - Shutdown handling forces wakeups of all waiters
3. **Async Integration**:
   - `readiness()` future manages waiter registration
   - Per-direction polling (read/write) through `poll_readiness`

## Safety Considerations
- Uses `UnsafeCell` and manual pointer management for intrusive lists
- Implements `Send`/`Sync` explicitly where safe
- Careful lock scoping to prevent holding across await points
- Memory ordering (Acquire/Release semantics) for atomic operations
