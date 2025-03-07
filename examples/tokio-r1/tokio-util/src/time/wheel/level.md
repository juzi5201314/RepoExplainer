# Timer Wheel Level Implementation

## Purpose
This file implements a single level in a hierarchical timer wheel used for efficiently managing timed events in the Tokio runtime. Each level tracks timers within a specific time range using a bitmask-optimized slot system.

## Key Components

### `Level<T>` Struct
- **Core Structure**: Represents a single timer wheel level with:
  - `level`: Hierarchy depth (0 = finest granularity).
  - `occupied`: Bitmask (64 bits) tracking occupied slots.
  - `slot`: Array of 64 slots storing timer entries (generic `T` implementing `Stack`).

### `Expiration` Struct
- **Tracking Mechanism**: Contains:
  - `level`: Which wheel level this expiration belongs to
  - `slot`: Index within the level
  - `deadline`: Absolute time when slot should be processed

### Constants & Helpers
- `LEVEL_MULT`: 64 (critical for bitwise operations)
- `slot_for()`: Computes slot index using bit shifting and modulo
- `slot_range()`/`level_range()`: Calculate time ranges per level

## Core Functionality

### Slot Management
1. **Next Expiration Calculation** (`next_expiration()`):
   - Uses bitwise rotation to find next occupied slot
   - Handles time wrapping for top-level pseudo-ring buffer behavior

2. **Entry Manipulation**:
   - `add_entry()`/`remove_entry()`: Modify slots and update occupancy bitmask
   - `pop_entry_slot()`: Retrieves entries while maintaining bitmask accuracy

### Bitwise Optimization
- `occupied` bitfield enables O(1) checks for empty levels
- Rotate-right + trailing zeros calculation efficiently finds next active slot

## Integration with Timer System
- Part of multi-level hierarchy where lower levels handle finer time granularities
- Higher levels manage exponentially larger time ranges (64ms → ~4min)
- Works with parent `Wheel` structure coordinating multiple levels

## Testing
- `slot_for()` verification ensures proper time-to-slot mapping
- Tests validate bitwise calculations for different hierarchy levels

# Role in Project