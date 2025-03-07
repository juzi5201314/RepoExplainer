# Timing Wheel Implementation in Tokio Runtime

## Purpose
This file implements a hierarchical hashed timing wheel used by Tokio's runtime to manage timer entries efficiently. It provides the core mechanism for scheduling and expiring asynchronous timers with high performance and precision (1ms granularity).

## Key Components

### `Wheel` Structure
- **Hierarchical Levels**: Contains 6 levels (each with 64 slots) tracking time ranges from 1ms up to ~2 years.
- **Elapsed Tracking**: Maintains `elapsed` time in milliseconds since creation.
- **Pending Entries**: Manages a list of entries ready to fire (`EntryList`).

### Core Algorithms
1. **Insertion**:
   - Determines appropriate level using `level_for()` based on deadline proximity.
   - Uses bitwise operations and leading zero counts to calculate expiration level.
   - Validates deadlines against current elapsed time.

2. **Expiration Processing**:
   - `poll()` method advances the wheel's time and processes expired entries.
   - Uses cascading expiration - entries move through levels until reaching the final slot.

3. **Efficiency Features**:
   - O(1) insertion/removal complexity through hashed slots.
   - Batch processing of expired timers during each poll cycle.

### Critical Constants
- `NUM_LEVELS = 6`: Determines wheel depth and maximum trackable duration
- `MAX_DURATION = (1 << (6*6)) - 1`: ~2 years maximum timeout duration

## Integration with Tokio
- Backs core timing primitives (`Sleep`, `Timeout`, `DelayQueue`)
- Used by runtime's time driver to manage thousands of concurrent timers
- Enables efficient timer management through hierarchical organization:
  - Level 0: 1ms slots (0-64ms)
  - Level 1: 64ms slots (64ms-4.1s)
  - Level 2: ~4.1s slots (4.1s-4.55min)
  - Higher levels follow similar exponential scaling

## Safety Considerations
- Uses unsafe blocks for intrusive linked list management
- Requires careful pinning/ownership management of timer entries
- Implements debug assertions to validate timing invariants

## Testing
- Contains validation for level calculation logic
- Verifies correct level assignment across time ranges
- Ensures proper cascading behavior between levels
