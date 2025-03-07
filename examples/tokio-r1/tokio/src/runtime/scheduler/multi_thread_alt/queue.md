# Tokio Multi-Thread Scheduler Work-Stealing Queue

## Purpose
This module implements a concurrent work-stealing queue for Tokio's multi-threaded scheduler. It enables efficient task distribution across worker threads by allowing idle threads to steal tasks from busy threads' queues, ensuring load balancing and CPU utilization.

## Key Components

### Core Structures
- **`Local<T>`**: Producer handle for single-threaded task insertion
- **`Steal<T>`**: Consumer handle for multi-threaded task stealing
- **`Inner<T>`**: Shared queue implementation containing:
  - Atomic head/tail indices
  - Ring buffer of task slots
  - Mask for fast modulo operations

### Concurrency Mechanisms
- **Atomic Operations**: Uses `AtomicUnsignedLong` and `AtomicUnsignedShort` for lock-free synchronization
- **Double-Word CAS**: Head field combines:
  - `steal` (MSB): Tracks in-progress steal operations
  - `real` (LSB): Actual queue head index
- **ABA Prevention**: Wider integer types (u64/u32) for indices to reduce wrap-around issues

### Main Operations
1. **Task Insertion** (`push_back*` methods):
   - Direct insertion when space available
   - Overflow handling moves half the queue to global storage
   - Batch operations for efficiency

2. **Task Retrieval** (`pop`):
   - Optimistic lock-free removal from local queue
   - Head index management for concurrent access

3. **Work Stealing** (`steal_into`):
   - Atomic claim of task range using CAS
   - Batched transfer to thief's queue
   - Coordinated head updates to prevent conflicts

### Safety Features
- **UnsafeCell** for controlled mutable access to task slots
- **MaybeUninit** for explicit memory management
- Loom-aware synchronization primitives
- Strict capacity checks and panic guarantees

## Integration with Tokio Runtime
- Part of the `multi_thread_alt` scheduler implementation
- Interfaces with:
  - Global injection queue via `Overflow` trait
  - Worker statistics tracking
  - Task lifecycle management
- Enables core scheduler behaviors:
  - Local task processing
  - Work balancing through stealing
  - Overflow handling under load

## Performance Considerations
- Ring buffer design for cache efficiency
- Batched steal operations reduce contention
- Optimized for common case (local processing)
- Fallback to global queue when overloaded
- Metrics collection for runtime observability

---
