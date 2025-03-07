# Tokio's `OnceCell` Implementation

## Purpose
This file implements a thread-safe, asynchronous `OnceCell` type for Tokio, designed to store a value that can be initialized exactly once. It enables safe concurrent access in asynchronous environments, supporting scenarios like lazy initialization of global/static resources where the initialization process itself may be asynchronous.

## Key Components

### Core Struct
- **`OnceCell<T>`**: The primary type containing:
  - `value_set: AtomicBool`: Atomic flag indicating initialization status.
  - `value: UnsafeCell<MaybeUninit<T>>`: Storage for the value (with thread-safe interior mutability).
  - `semaphore: Semaphore`: Tokio semaphore to coordinate exclusive write access.

### Key Mechanisms
1. **Atomic Synchronization**:
   - Uses `AtomicBool` to track initialization state with atomic operations (`Ordering::Acquire/Release`).
   - Ensures visibility of writes across threads.

2. **Semaphore Coordination**:
   - A 1-permit semaphore enforces exclusive access during initialization.
   - Closed semaphore after initialization optimizes read access.

3. **Memory Safety**:
   - `UnsafeCell` provides interior mutability while adhering to Rust's safety rules.
   - `MaybeUninit` handles uninitialized memory safely.

### Main Functionality
- **Initialization**:
  - `get_or_init()`: Async method that either returns an initialized value or runs an async initializer.
  - `set()`: Synchronous attempt to initialize (fails if already initialized).

- **Concurrent Access**:
  - Safe concurrent reads after initialization.
  - Atomic checks and semaphore coordination prevent race conditions during writes.

- **Destruction**:
  - `Drop` implementation ensures proper cleanup of initialized values.
  - `into_inner()`/`take()` for ownership transfer.

### Error Handling
- **`SetError`**: Returned from failed `set()` attempts, with variants:
  - `AlreadyInitializedError`: Value already exists.
  - `InitializingError`: Concurrent initialization in progress.

## Integration with Tokio
- **Async Runtime Integration**:
  - Uses Tokio's `Semaphore` for async-compatible locking.
  - Works with Tokio's instrumentation (via `crate::trace` in async methods).

- **Thread Safety**:
  - Implements `Sync` (for thread-safe shared access) and `Send` (for cross-thread transfers) where appropriate.
  - Integrates with Tokio's `loom` testing model for concurrency validation.

## Example Usage
```rust
static GLOBAL: OnceCell<u32> = OnceCell::const_new();

async fn get_value() -> &'static u32 {
    GLOBAL.get_or_init(|| async { compute_value().await }).await
}
```

## Safety Considerations
- **Invariants**:
  - Semaphore closure strictly follows `value_set = true`.
  - Unsafe blocks are carefully guarded by atomic checks and semaphore state.

- **Panic Handling**:
  - Aborted initializations release the semaphore permit, allowing retries.

This file provides a foundational synchronization primitive for one-time async-safe initialization in Tokio-based applications.  