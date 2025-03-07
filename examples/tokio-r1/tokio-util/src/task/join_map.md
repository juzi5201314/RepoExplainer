# `tokio_util/src/task/join_map.rs` Explanation

## Purpose
The `JoinMap` struct extends Tokio's task management capabilities by associating spawned tasks with hash map keys. It combines the functionality of `JoinSet` (managing async tasks) with key-based operations like cancellation and lookup, while tracking task results with their corresponding keys.

## Key Components

### Core Structures
- **`JoinMap<K, V, S>`**: Main struct storing:
  - `tasks_by_key`: HashMap linking composite `Key<K>` (user key + task ID) to `AbortHandle`
  - `hashes_by_task`: Reverse map from task IDs to key hashes for efficient lookups
  - `tasks`: Inner `JoinSet<V>` managing task execution

- **`Key<K>`**: Internal type combining user-provided key `K` and task `Id` to resolve hash collisions.

### Key Functionality
1. **Task Spawning**:
   - Methods like `spawn()`, `spawn_blocking()`, and `spawn_local()` insert tasks while handling key conflicts (aborting existing tasks with same key).
   - Uses double hashing strategy for O(1) lookups by key or task ID.

2. **Task Management**:
   - `join_next()`: Awaits next completed task, returns (key, result) pair while cleaning up internal maps.
   - `abort()`/`abort_matching()`: Cancel tasks by key or predicate.
   - `shutdown()`: Aborts all tasks and awaits their termination.

3. **Container Operations**:
   - Capacity management (`reserve()`, `shrink_to_fit()`)
   - Key iteration (`keys()`) and existence checks (`contains_key()`)

### Hashing Strategy
- Custom `Key<K>` hashing ignores task IDs to enable key-based lookups
- Uses `hashbrown` for raw hash API access to handle collisions via task ID comparison

## Integration with Tokio
- Built on Tokio's `JoinSet` for task execution tracking
- Integrates with runtime handles and `LocalSet` for different execution contexts
- Requires Tokio's unstable features (task IDs) for precise task control

## Example Use Cases
- Managing parallel requests with unique identifiers
- Implementing task timeouts/retries using key-based cancellation
- Batch processing with per-item result tracking

## Role in Project