# Tokio Synchronization Primitives Module (`sync/mod.rs`)

## Purpose
This module provides asynchronous synchronization primitives for coordinating tasks in Tokio's concurrent execution model. It offers both message-passing channels and state synchronization utilities designed for async/await contexts.

## Key Components

### Message Passing Channels
1. **Oneshot**:
   - Single-producer/single-consumer channel for one-time value passing
   - Used for request-response patterns and task result delivery

2. **MPSC** (Multi-Producer Single-Consumer):
   - Buffered channel for streaming multiple values
   - Supports backpressure through configurable capacity
   - Used for work queues and producer/consumer patterns

3. **Broadcast**:
   - Multi-producer/multi-consumer channel for fan-out patterns
   - All consumers receive all messages
   - Useful for pub-sub systems

4. **Watch**:
   - Single-value broadcast channel tracking latest state
   - Consumers get current value and notified of changes
   - Ideal for configuration updates and state monitoring

### State Synchronization
1. **Mutex/RwLock**:
   - Async versions of mutual exclusion primitives
   - Support cooperative scheduling to prevent task starvation

2. **Semaphore**:
   - Limits concurrent access to resources
   - Used for rate limiting and resource pooling

3. **Barrier**:
   - Coordinates multiple tasks to wait for collective progress

4. **Notify**:
   - Basic task wakeup mechanism without data transfer

## Design Features
- **Runtime Agnostic**: Works with any executor, not just Tokio
- **Cooperative Scheduling**: Integrates with Tokio's task system to prevent starvation
- **Conditional Compilation**: Selectively includes components based on enabled features
- **Documentation Focus**: Extensive examples and usage patterns in module docs

## Integration with Project
This module serves as the foundation for Tokio's concurrency model:
- Used by higher-level I/O components (TCP, UDP, filesystem)
- Essential for task coordination in async contexts
- Provides building blocks for stream processing and parallel computation
- Integrates with Tokio's task system for efficient scheduling

## Key Implementation Details
- Uses loom for concurrency testing
- Implements custom atomic operations and linked lists for queue management
- Provides both owned and borrowed guard types for resource safety
- Supports `no_std` environments through conditional compilation
