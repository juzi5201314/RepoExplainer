# DelayQueue Implementation in Tokio-util

## Purpose
The `delay_queue.rs` file implements a `DelayQueue` structure, which is a time-aware queue that holds elements until their specified expiration deadlines. It's designed for efficiently managing and processing delayed items in asynchronous Rust applications, such as handling timeouts, scheduling tasks, or cache evictions.

## Key Components

### 1. **Core Structures**
- **`DelayQueue<T>`**: Main queue type storing delayed elements.
  - `slab`: `SlabStorage<T>` for memory-efficient storage.
  - `wheel`: Timer wheel for tracking expiration deadlines.
  - `expired`: Stack for immediately available expired items.
  - `delay`: Future for the next expiration event.
- **`SlabStorage<T>`**: Manages storage using a slab allocator with:
  - `inner`: Slab for data storage.
  - `key_map`: Tracks key remapping after compaction.
- **`Key`/`KeyInternal`**: Handles for accessing queue entries.

### 2. **Timer Wheel**
- Hierarchical timer wheel from `crate::time::wheel` for O(1) insertion/expiration of timers.
- Organizes deadlines into time buckets for efficient polling.

### 3. **Expiration Handling**
- **Expired Stack**: Holds items past their deadlines for immediate access.
- **Normalization**: Converts `Instant` deadlines to wheel-compatible millisecond offsets.

### 4. **Key Features**
- **Insertion**: `insert()`/`insert_at()` for adding items with durations/absolute times.
- **Polling**: `poll_expired()` async method to retrieve expired items.
- **Mutation**: `remove()`, `reset()`, and `reset_at()` for dynamic deadline adjustments.
- **Memory Management**: `shrink_to_fit()`, `compact()`, and slab-based allocation.

## Key Methods
- **`insert_at`**: Adds an item with an absolute deadline.
- **`poll_expired`**: Async method yielding expired items.
- **`remove`/`reset`**: Modify queue entries using `Key`.
- **`peek`**: Inspects the next expiring item without removal.

## Integration with Tokio
- Uses Tokio's `sleep_until` for efficient delay tracking.
- Implements `futures_core::Stream` for async iteration over expired items.
- Integrates with Tokio's task wakeup system via `Waker`.

## Performance Considerations
- **Timer Wheel**: Efficiently manages thousands of timers with minimal overhead.
- **Slab Allocator**: Reduces memory fragmentation and allocation costs.
- **Key Remapping**: Preserves key validity after slab compaction.

## Example Use Case
```rust
// Cache with TTL using DelayQueue
struct Cache {
    entries: HashMap<CacheKey, (Value, Key)>,
    expirations: DelayQueue<CacheKey>,
}

impl Cache {
    fn insert(&mut self, key: CacheKey, value: Value) {
        let delay = self.expirations.insert(key.clone(), Duration::from_secs(30));
        self.entries.insert(key, (value, delay));
    }

    fn poll_purge(&mut self, cx: &mut Context<'_>) -> Poll<()> {
        while let Some(entry) = ready!(self.expirations.poll_expired(cx)) {
            self.entries.remove(entry.get_ref());
        }
        Poll::Ready(())
    }
}
```

## Role in Project