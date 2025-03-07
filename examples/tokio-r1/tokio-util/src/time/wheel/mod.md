# Timing Wheel Implementation in Tokio

## Purpose
This file implements a hierarchical hashed timing wheel used to manage and expire timers efficiently. It forms the core timing mechanism for Tokio's asynchronous timer facilities like `DelayQueue`, `Sleep`, and `Timeout`, enabling precise timer management over long durations (up to 2 years) with millisecond granularity.

## Key Components

### 1. Wheel Structure
```rust
pub(crate) struct Wheel<T> {
    elapsed: u64,
    levels: Box<[Level<T>]>,
}
```
- **elapsed**: Tracks milliseconds since creation
- **levels**: 6-tier hierarchical structure where each level handles exponentially larger time ranges

### 2. Level Hierarchy
Each level contains 64 slots with increasing time ranges:
1. Level 0: 1ms slots / 64ms range
2. Level 1: 64ms slots / ~4s range
3. Level 2: ~4s slots / ~4min range
4. Level 3: ~4min slots / ~4hr range
5. Level 4: ~4hr slots / ~12 day range
6. Level 5: ~12 day slots / ~2 year range

### 3. Core Operations
- **insert()**: Adds timers to appropriate level
- **poll()**: Advances time and processes expired timers
- **level_for()**: Determines correct level for a timestamp
- **poll_expiration()**: Cascades timers between levels

### 4. Time Calculation
```rust
fn level_for(elapsed: u64, when: u64) -> usize {
    // Uses bitmasking and leading zero count to determine level
}
```
Efficiently calculates the appropriate level using bitwise operations and leading zero counts.

## Integration with Tokio
1. **Timer Backing**: Used by `Timer` and `DelayQueue` for timeout management
2. **Storage Abstraction**: Works with generic `Stack` trait for flexible storage (heap/slab)
3. **Efficiency**: Minimizes operations through hierarchical design (O(1) insert/remove in most cases)
4. **Precision**: Maintains millisecond accuracy while handling long durations

## Key Algorithms
1. **Hierarchical Cascading**: Timers trickle down through levels as time progresses
2. **Expiration Tracking**: Efficiently finds next expiration using level-based checking
3. **Time Masking**: Uses bitwise operations for fast level/slot calculations

## Error Handling
Defines `InsertError` with variants:
- `Elapsed`: When timer expiration is in the past
- `Invalid`: When expiration exceeds maximum duration (2 years)

## Testing
Contains validation for level calculation logic to ensure correct timer placement across the hierarchy.
