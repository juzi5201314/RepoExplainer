# Timeout Stream Extension

## Purpose
This file implements a `Timeout` stream wrapper that adds timeouts to an underlying async stream. It ensures stream items are produced within specified durations, returning `Elapsed` errors when timeouts occur between items.

## Key Components

### `Timeout<S>` Struct
- **Wraps**: 
  - `Fuse<S>`: Ensures terminated streams stay terminated
  - `Sleep`: Tokio's timer future for deadline tracking
- **State**:
  - `duration`: Timeout interval
  - `poll_deadline`: Flag controlling timer checks

### Core Logic (`poll_next`)
1. **Check Stream First**:
   - Returns immediately if stream yields item
   - Resets timer on successful item reception
2. **Timeout Handling**:
   - Checks timer only after stream returns `Pending`
   - Returns `Elapsed` error if timer expires

### Error Handling
- `Elapsed` error type:
  - Implements `Display`, `Error`, and conversion to `std::io::Error`
  - Provides clear timeout indication

### Size Hint
- Modifies upper bound to account for potential timeout errors between items (2x+1 multiplier)

## Integration with Project
- Part of Tokio's stream utilities (`StreamExt` extension trait)
- Complements other timeout-related utilities (`TimeoutRepeating`, `chunks_timeout`)
- Used via `stream.timeout(duration)` pattern
- Integrates with Tokio's time system for accurate async timing

## Role in Project
Provides stream timeout functionality for the Tokio async runtime, enabling time-bound processing of stream elements with proper error handling.
