# Tokio Mutex Implementation

## Purpose
This file implements an asynchronous Mutex for the Tokio runtime, providing thread-safe mutual exclusion in async contexts. It allows tasks to lock shared data without blocking the executor thread, enabling concurrency across async/await points.

## Key Components

### 1. Core Structures
- **`Mutex<T>`**: Main mutex type containing:
  - `Semaphore` for FIFO lock queuing
  - `UnsafeCell<T>` for protected data
  - Tracing spans for diagnostics (when enabled)
  
- Guard Types:
  - `MutexGuard`: Borrowed lock guard
  - `OwnedMutexGuard`: Arc-owned version with 'static lifetime
  - `MappedMutexGuard`: Projected view into locked data
  - `OwnedMappedMutexGuard`: Owned version of mapped guard

### 2. Locking Mechanisms
- **Async Locking**: Uses semaphore acquisition with async/await
- **Blocking Variants**: `blocking_lock` for sync contexts
- **Try Lock**: Immediate acquisition attempt
- **Owned Locks**: Work with Arc-wrapped mutexes for static lifetime

### 3. Key Features
- FIFO fairness for lock acquisition
- Zero poisoning (unlocks on panic)
- Mutable access projection via map/try_map
- Tracing integration for async diagnostics
- Thread safety through Send/Sync implementations

### 4. Implementation Details
- Uses a binary semaphore (count=1) for lock state
- Implements drop guards for automatic unlocking
- Provides Deref/DerefMut for ergonomic data access
- Includes blocking->async bridge functionality

## Project Integration
This implementation:
- Complements other sync primitives (RwLock, Semaphore)
- Integrates with Tokio's task system through async locking
- Supports both borrowed and owned locking patterns
- Works with Tokio's tracing infrastructure
- Follows Tokio's error handling patterns (TryLockError)

## Safety Considerations
- UnsafeCell for interior mutability
- Manual Drop implementations for guard types
- Proper Send/Sync trait implementations
- Memory ordering guarantees through loom verification

## Example Usage
```rust
let mutex = Arc::new(Mutex::new(0));
let guard = mutex.lock().await;
*guard += 1;
```
