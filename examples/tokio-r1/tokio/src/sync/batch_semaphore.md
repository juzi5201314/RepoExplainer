# Tokio Batch Semaphore Implementation

## Purpose
This file implements an asynchronous counting semaphore that allows tasks to wait for multiple permits. It's designed to ensure fairness, preventing starvation in scenarios like read-write locks by using an intrusive linked list to manage waiters.

## Key Components

### Core Structures
- **`Semaphore`**: Main semaphore type containing:
  - `permits`: Atomic counter tracking available permits (with bitflags for closed state)
  - `waiters`: Mutex-protected wait list
  - Tracing support for diagnostics
- **`Waitlist`**: Managed queue of waiting tasks:
  - `queue`: Intrusive linked list of `Waiter` nodes
  - `closed`: Flag indicating semaphore closure
- **`Waiter`**: Represents a waiting task:
  - Tracks required permits and contains wake-up mechanism
  - Intrusive list pointers for queue management
  - Thread-safe state management using atomics

### Key Mechanisms
1. **Fair Queue Management**:
   - Waiters are added to the end of a linked list and served from the front
   - Ensures tasks requesting large permit counts eventually get serviced

2. **Atomic Permit Tracking**:
   - Uses bit shifting to store state flags (closed status)
   - Implements `MAX_PERMITS` limit (usize::MAX >> 3)

3. **Async Acquisition**:
   - `Acquire` future handles asynchronous permit requests
   - Implements proper cleanup on drop to prevent leaks

4. **Efficient Permit Distribution**:
   - `add_permits_locked` distributes permits to waiters while maintaining lock safety
   - Leftover permits are returned to the semaphore counter

## Critical Methods
- `release()`: Adds permits and wakes waiting tasks
- `close()`: Marks semaphore closed and wakes all waiters
- `try_acquire()`: Immediate permit attempt
- `poll_acquire()`: Core async acquisition logic
- `forget_permits()`: Non-blocking permit reduction

## Concurrency Safety
- Uses `loom` primitives for thread-safe atomic operations
- Implements proper memory ordering (Acquire/Release semantics)
- Handles concurrent access through mutex-protected wait list

## Integration with Tokio
- Foundation for higher-level synchronization primitives:
  - Used in Mutex, RwLock, and other concurrency tools
- Enables fair resource distribution across async tasks
- Integrates with Tokio's tracing infrastructure for observability

## Error Handling
- `TryAcquireError`: Differentiates between closed state and lack of permits
- `AcquireError`: Specialized error for async acquisition failures

## Performance Considerations
- Intrusive linked list minimizes allocations
- Lock contention minimized through atomic permit checks
- Batch permit handling improves throughput
