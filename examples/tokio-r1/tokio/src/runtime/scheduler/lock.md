# Tokio Runtime Scheduler Lock Implementation

## Purpose
This file defines a generic locking abstraction (`Lock` trait) and concrete synchronization primitives (like `Mutex`) used in Tokio's runtime scheduler. It provides thread-safe access to shared resources while supporting different concurrency models (multi-threaded vs single-threaded).

## Key Components

### 1. Lock Trait
```rust
pub(crate) trait Lock<T> {
    type Handle: AsMut<T>;
    fn lock(self) -> Self::Handle;
}
```
- Generic abstraction over synchronization primitives
- `Handle` ensures locked data can be accessed mutably
- Allows different lock implementations through trait polymorphism

### 2. Mutex Implementation
```rust
pub(crate) struct Mutex<T>(sync::Mutex<T>);
```
- Wrapper around standard library's `Mutex` with Tokio-specific enhancements
- Key methods:
  - `new()`: Creates a new mutex
  - `lock()`: Blocks until lock is acquired
  - `try_lock()`: Non-blocking lock attempt
  - `blocking_lock()`: Async-compatible blocking lock

### 3. Concurrency Control Features
- `wait()` and `wait_timeout()`: Condition variable-like functionality
- Loom integration (`loom::sync::Mutex`) for concurrency testing
- AtomicU64 support for efficient atomic operations

### 4. Specialized Implementations
```rust
impl<'a> Lock<Synced> for &'a mut Synced {
    type Handle = &'a mut Synced;
    //...
}
```
- Optimization for single-threaded contexts where actual locking isn't needed
- Allows using direct mutable references instead of full mutexes

## Integration with Tokio Runtime
- Provides synchronization primitives for the scheduler's work-stealing algorithm
- Enables safe task queue access across worker threads
- Supports both multi-threaded and current-thread runtime flavors
- Forms foundation for task scheduling and resource management

## Design Considerations
- Abstraction allows runtime configuration of synchronization strategy
- Loom integration ensures correct concurrency behavior
- Zero-cost abstractions for single-threaded use cases
- Ergonomic API bridging async and blocking code paths
