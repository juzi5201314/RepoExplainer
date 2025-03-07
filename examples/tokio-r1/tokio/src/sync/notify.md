# Tokio `Notify` Synchronization Primitive

## Purpose
The `notify.rs` file implements the `Notify` synchronization primitive, which allows a single task to notify another task when an event occurs. It serves as a foundational building block for coordinating asynchronous tasks in Tokio, enabling efficient wakeup signaling without data transfer.

## Key Components

### 1. Core Structures
- **`Notify`**: Main synchronization primitive containing:
  - `state`: Atomic integer tracking state (EMPTY, WAITING, NOTIFIED) + notification counters.
  - `waiters`: Mutex-protected intrusive linked list of pending waiters (`Waiter` nodes).
  
- **`Waiter`**: Represents a waiting task with:
  - Intrusive list pointers.
  - Atomic notification state.
  - Waker for task wakeup.
  - `PhantomPinned` to ensure safe pinning.

### 2. Notification States
- **EMPTY**: No pending notifications or waiters.
- **WAITING**: Active waiters present.
- **NOTIFIED**: Permit available for immediate wakeup.

### 3. Notification Strategies
- **`notify_one()`**: Wakes oldest waiter (FIFO).
- **`notify_last()`**: Wakes newest waiter (LIFO).
- **`notify_waiters()`**: Wakes all current waiters atomically.

### 4. `Notified` Future
Returned by `Notify::notified()`, this future:
- Manages registration in the wait list.
- Handles state transitions between `Init`, `Waiting`, and `Done`.
- Implements proper cleanup on drop to prevent resource leaks.

## Concurrency Control
- Uses atomic operations for state management with SeqCst ordering.
- Leverages `loom`-aware synchronization primitives for concurrency testing.
- Intrusive linked list minimizes allocations and allows lock-free operations in some paths.

## Critical Algorithms
- **Notification Handling**: 
  - `notify_locked()` dequeues waiters based on strategy (FIFO/LIFO).
  - Atomic state transitions ensure correct permit handling.
  
- **Wait List Management**:
  - `NotifyWaitersList` guards against lost wakeups during batch notifications.
  - Safe waiter removal during future drops.

## Integration with Tokio
- Used internally to implement higher-level primitives like channels and task queues.
- Enables efficient task wakeup without spinning or busy-waiting.
- Works with Tokio's executor to schedule tasks when notified.

## Safety Considerations
- **Thread Safety**: Implements `Send`/`Sync` correctly using atomic operations and locked regions.
- **Memory Safety**: Intrusive list operations use `NonNull` and careful lifetime management.
- **Panic Safety**: Waker operations protected against panics during notification.

## Example Use Cases
1. **MPSC Channels**: Coordinating producer/consumer without data races.
2. **Task Coordination**: Signaling between async tasks in pipeline patterns.
3. **Batch Processing**: Using `notify_waiters` for bulk wakeups.

## Key Optimizations
- Permit caching to avoid unnecessary syscalls.
- Intrusive lists minimize memory overhead.
- Atomic state packing reduces cache line usage.

---
