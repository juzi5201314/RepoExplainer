# Tokio Task Containers: `OwnedTasks` and `LocalOwnedTasks`

## Purpose
This module provides thread-safe (`OwnedTasks`) and non-thread-safe (`LocalOwnedTasks`) containers for managing tasks spawned in a Tokio scheduler. These structures ensure proper task lifecycle management, including ownership tracking, shutdown coordination, and thread-safety guarantees.

## Key Components

### 1. **OwnedTasks**
- **Thread Safety**: Uses a sharded linked list (`ShardedList`) to minimize lock contention.
- **Key Features**:
  - Unique `id` (via atomic counter) to verify task ownership.
  - Atomic `closed` flag to prevent new tasks during shutdown.
  - Methods for binding tasks (`bind`/`bind_local`), asserting ownership (`assert_owner`), and bulk shutdown (`close_and_shutdown_all`).
- **Sharding**: Dynamically adjusts shard count based on core count to balance memory locality and concurrency.

### 2. **LocalOwnedTasks**
- **Single-Threaded**: Uses a non-thread-safe `LinkedList` inside an `UnsafeCell`.
- **Key Features**:
  - Supports non-`Send` tasks (unlike `OwnedTasks`).
  - Similar interface to `OwnedTasks` but without atomic operations.
  - Accessed via `with_inner` to ensure thread-local safety.

## Core Functionality
- **Task Binding**:
  - Assigns a unique owner ID to tasks during creation.
  - Rejects new tasks if the container is closed.
- **Shutdown**:
  - `close_and_shutdown_all` iterates through tasks, triggering their shutdown sequence.
  - Prevents new task additions via the `closed` flag.
- **Ownership Verification**:
  - `assert_owner` checks task IDs to ensure safe polling.
- **Memory Management**:
  - Uses intrusive linked lists for efficient task storage/removal.

## Integration with Tokio Runtime
- **Task Lifecycle**: These containers track all runtime tasks, enabling coordinated shutdown during runtime termination.
- **Scheduler Coordination**: Works with Tokio's scheduler components (e.g., `Inject`, `Defer`) to manage task queues.
- **Metrics**: Optional 64-bit metrics track spawned tasks (enabled via `cfg_64bit_metrics`).

## Safety Considerations
- **Atomic Operations**: `OwnedTasks` uses atomic flags and counters for thread-safe state management.
- **UnsafeCell**: `LocalOwnedTasks` relies on `UnsafeCell` for interior mutability, assuming single-threaded access.
- **ID Collision Prevention**: Atomic ID generation ensures unique ownership identifiers across runtime instances.

## Testing
- **ID Generation Test**: Verifies that IDs are strictly increasing to prevent cross-runtime task mixups.

---
