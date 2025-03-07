# Tokio Scheduler Injection Queue (Shared Implementation)

## Purpose
This file implements a thread-safe injection queue for Tokio's multi-threaded scheduler. It provides a shared task queue where tasks can be added by producers and stolen by worker threads when their local queues are empty.

## Key Components

### `Shared<T>` Struct
- **Atomic Length Tracking**: Uses `AtomicUsize` to maintain queue length for lock-free size checks
- **PhantomData**: Type marker for generic task type `T`
- **Thread Safety**: Implements `Send` and `Sync` for cross-thread usage

### `Synced` Structure (from context)
- Contains actual queue state protected by a lock:
  - `is_closed`: Queue shutdown flag
  - `head/tail`: Linked list pointers for task storage

### Core Operations
1. **Push Operation**:
   - Converts tasks to raw pointers for linked list management
   - Atomically increments length counter
   - Handles queue closure checks

2. **Pop Operations**:
   - `pop()`: Removes single task
   - `pop_n()`: Batched removal of multiple tasks
   - Uses atomic decrements for length updates

3. **Concurrency Control**:
   - Combines atomic operations for fast path checks
   - Requires synchronized access to `Synced` for mutations
   - Implements closure protocol for graceful shutdown

## Integration with Tokio Runtime
- Part of scheduler's work-stealing mechanism
- Interfaces with worker threads through `Synced` locks
- Coordinates with other scheduler components like:
  - Multi-threaded worker cores
  - Task dumping functionality
  - Shutdown procedures

## Performance Considerations
- Atomic length counter minimizes locking overhead
- Batch operations reduce synchronization frequency
- Linked list structure enables efficient FIFO operations
- Separation of atomic metadata (Shared) and locked state (Synced) optimizes hot paths
