# PollSemaphore Implementation Explanation

## Purpose
The `poll_semaphore.rs` file provides a wrapper around Tokio's `Semaphore` to enable asynchronous polling for permits. It bridges Tokio's semaphore functionality with futures-based workflows, allowing integration with async streams and poll-based operations.

## Key Components

### Struct `PollSemaphore`
- **Fields**:
  - `semaphore`: An `Arc<Semaphore>` for thread-safe reference counting.
  - `permit_fut`: An optional tuple storing:
    - The number of permits requested (`u32`).
    - A reusable future (`ReusableBoxFuture`) for permit acquisition.

### Core Methods
1. **Construction**:
   - `new()`: Initializes with a `Semaphore` instance.
   - `close()`: Closes the semaphore to prevent further permits.
   - `clone_inner()`/`into_inner()`: Manage access to the underlying semaphore.

2. **Polling Logic**:
   - `poll_acquire()`: Requests 1 permit via `poll_acquire_many()`.
   - `poll_acquire_many()`: Core method for asynchronous permit acquisition:
     - Reuses or replaces futures when permit counts change.
     - Handles immediate acquisition via `try_acquire_many_owned()`.
     - Manages task wakeups and semaphore closure detection.

3. **Utility Methods**:
   - `available_permits()`: Delegates to the inner semaphore's permit count.
   - `add_permits()`: Adds permits to the semaphore.

### Trait Implementations
- **`Stream`**: Allows `PollSemaphore` to act as a stream of `OwnedSemaphorePermit` via `poll_next()`.
- **`Clone`/`Debug`**: Standard implementations for cloning/debugging.
- **`AsRef<Semaphore>`**: Provides direct access to the inner semaphore.

## Integration with the Project
- Bridges Tokio's synchronization primitives with futures-based async workflows.
- Enables non-blocking integration of semaphores in async streams, task schedulers, or resource pools.
- Used in contexts requiring backpressure or concurrency limits (e.g., async network handlers, file I/O).

---
