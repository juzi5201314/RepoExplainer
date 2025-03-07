# ShardedList Implementation in Tokio

## Purpose
The `ShardedList` provides a concurrent, sharded intrusive linked list designed to minimize lock contention in high-throughput scenarios. It splits data into multiple shards (each protected by its own mutex) to allow parallel operations across different shards while maintaining thread safety.

## Key Components

### 1. Core Structures
- **`ShardedList<L, T>`**: Main container with:
  - `lists`: Array of mutex-guarded `LinkedList` shards
  - `added`/`count`: Atomic metrics tracking total insertions and current size
  - `shard_mask`: Bitmask for efficient shard selection
- **`ShardGuard`**: RAII guard providing exclusive access to a specific shard while maintaining metrics

### 2. Trait Contracts
- **`ShardedListItem`**: Safety-critical trait requiring:
  - Stable shard ID calculation via `get_shard_id`
  - Pointer validity guarantees for concurrent operations

### 3. Concurrency Mechanisms
- **Shard Locking**: Per-shard mutexes enable fine-grained locking
- **Atomic Counters**: `MetricAtomicU64`/`MetricAtomicUsize` for lock-free size tracking
- **Power-of-Two Sharding**: Enables fast modulo via bitwise AND (`id & shard_mask`)

## Key Operations
- **`push()`**: 
  - Locks appropriate shard via `lock_shard`
  - Updates metrics atomically
- **`pop_back()`/`remove()`**: 
  - Shard-specific removal with metric updates
  - Safety enforced through `ShardedListItem` invariants
- **`for_each()`** (taskdump feature): 
  - Bulk iteration across all shards
  - Requires locking all shards simultaneously

## Integration with Tokio
- Used in task scheduling and I/O management
- Implements sharding for `tokio::sync::mpsc` channels
- Supports task dumping functionality through iteration
- Integrates with Tokio's loom testing framework for concurrency validation

## Safety Considerations
- Relies on `ShardedListItem` implementers maintaining stable shard IDs
- Requires proper synchronization through shard guards
- Enforces power-of-two shard sizes for efficient bitmasking

## Performance Characteristics
- Reduces contention through shard partitioning
- Maintains O(1) complexity for shard selection
- Uses relaxed atomics for metrics where possible
