# ChunksTimeout Stream Implementation

## Purpose
Implements a stream that groups items into chunks based on either:
1. Reaching a maximum chunk size (`max_size`)
2. Elapsing of a specified duration timeout

This combines size-based batching with time-based flushing, useful for scenarios requiring periodic aggregation of data streams even when full batches aren't reached.

## Key Components

### Struct Definition
```rust
pub struct ChunksTimeout<S: Stream> {
    stream: Fuse<S>,       // Fused inner stream
    deadline: Option<Sleep>, // Timeout mechanism
    duration: Duration,    // Timeout duration
    items: Vec<S::Item>,   // Accumulated items
    cap: usize,            // Maximum chunk size
}
```

### Core Functionality
1. **Polling Logic** (`poll_next`):
   - Aggressively collects items until `max_size` is reached
   - Starts timeout timer on first received item
   - Emits chunk when either:
     - Batch reaches capacity (`max_size`)
     - Timeout elapses with pending items
     - Source stream completes

2. **Timeout Handling**:
   - Uses `tokio::time::Sleep` for async delays
   - Resets timer when new batch starts
   - Checks timeout expiration during stream pauses

3. **Resource Management**:
   - Pre-allocates vector capacity with `Vec::with_capacity`
   - Uses `std::mem::take` for zero-copy buffer swaps

## Integration with Project
- Part of Tokio's stream utilities (`StreamExt` trait)
- Complements other timeout-related stream operators (`timeout`, `timeout_repeating`)
- Works with fused streams to handle termination properly
- Used via `chunks_timeout` method in stream processing pipelines

## Size Hint Behavior
- Estimates chunk counts based on:
  - Remaining items in current batch
  - Inner stream's size hints divided by chunk capacity
- Provides lower/upper bounds for consumer optimization

## Typical Use Cases
- Batching network packets with size/time constraints
- Aggregating metrics with periodic flushing
- Implementing producer-side buffering in message queues
