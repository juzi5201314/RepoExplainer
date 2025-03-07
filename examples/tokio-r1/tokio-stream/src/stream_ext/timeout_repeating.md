# TimeoutRepeating Stream Implementation

## Purpose
Provides a stream wrapper that emits timeout errors at regular intervals when the underlying stream is inactive. Used to detect and handle periods of inactivity in asynchronous streams.

## Key Components

### Struct Definition
- `TimeoutRepeating<S>`: Pinned struct combining:
  - `stream: Fuse<S>`: Fused inner stream (prevents polling after termination)
  - `interval: Interval`: Repeating timer from Tokio's time module

### Core Functionality
- Implements `Stream` with `Item = Result<S::Item, Elapsed>`
- Polling behavior:
  1. Checks inner stream first
  2. Resets interval timer on new stream items
  3. Emits `Elapsed` error when interval triggers without stream activity
- Size hint preserves lower bound but removes upper bound (infinite potential timeouts)

### Key Methods
- `new()`: Initializes with stream and interval
- `poll_next()`: Implements dual-polling logic between stream and timer
- `size_hint()`: Provides stream size estimation

## Integration with Project
- Part of `StreamExt` extension traits in Tokio's streaming utilities
- Complements other timeout-related stream adapters (`timeout`, `ChunksTimeout`)
- Works with Tokio's time system to provide async-aware timing
- Used in scenarios requiring periodic liveness checks on streams
