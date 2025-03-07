# Tokio Scheduler Idle Management Module

## Purpose
This module coordinates worker thread idling in Tokio's multi-threaded scheduler. It manages:
- Tracking idle vs active worker threads
- Efficient worker wakeup notifications
- Core resource allocation between workers
- Shutdown coordination

## Key Components

### 1. Core Tracking Structures
- **`Idle`**: Main state manager with atomic counters:
  - `num_searching`: Workers looking for work
  - `num_idle`: Available worker cores
  - `idle_map`: Bitmap of idle cores
  - `needs_searching`: Flag for work redistribution

- **`IdleMap`**: Efficient bitmap storage using atomic usize chunks to track idle cores

- **`Synced`**: Mutex-protected state:
  - `sleepers`: IDs of parked workers
  - `available_cores`: Unassigned worker cores

### 2. State Transition Methods
- **Core Acquisition/Release**:
  - `try_acquire_available_core()` - Assigns cores to workers
  - `release_core()` - Returns cores to available pool

- **Worker Notifications**:
  - `notify_local()`/`notify_remote()` - Wake workers using condition variables
  - `notify_synced()` - Core notification logic under lock

- **State Transitions**:
  - `transition_worker_to_searching()` - Mark worker as task-searching
  - `transition_worker_from_searching()` - End search phase

### 3. Shutdown Handling
- `shutdown()`: Wake all workers with core assignments
- `shutdown_unassigned_cores()`: Cleanup remaining cores

## Concurrency Management
- Uses atomic operations (Acquire/Release ordering) for lock-free counters
- Leverages mutex-protected `Synced` for coordinated state changes
- Implements efficient bitmap operations for core tracking

## Integration with Scheduler
- Part of multi-threaded scheduler's worker management
- Interacts with:
  - Worker state management (`worker` module)
  - Task injection system (`inject`)
  - Core resource pool management
  - Shutdown coordination system

## Optimization Features
- Bitmap-based idle tracking for O(1) core lookups
- Atomic counter updates for minimal locking
- Work-stealing prevention through search worker limits
- False-negative prevention via `needs_searching` flag
