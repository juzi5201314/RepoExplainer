# Tokio's TryLock Implementation

## Purpose
Provides a non-blocking mutual exclusion primitive that allows threads to attempt lock acquisition without blocking. Designed for low-contention scenarios where immediate access is preferred over waiting.

## Key Components

### 1. Core Structures
- **`TryLock<T>`**: Main lock container
  - `locked: AtomicBool`: Atomic flag for lock state
  - `data: UnsafeCell<T>`: Thread-unsafe data container with interior mutability
- **`LockGuard<'a, T>`**: RAII guard for locked state
  - Contains reference to parent lock
  - Uses `PhantomData<std::rc::Rc<()>>` to prevent accidental Send implementation

### 2. Concurrency Safety
- Implements `Send`/`Sync` for `TryLock<T>` when `T: Send`
- Implements `Sync` for `LockGuard` when `T: Sync`
- Uses `AtomicBool::compare_exchange` with sequential consistency (SeqCst) for atomic lock acquisition

### 3. Locking Mechanism
- **Non-blocking try_lock()**:
  ```rust
  if compare_exchange(false, true) succeeds => Some(guard)
  else => None
  ```
- RAII guard automatically releases lock on drop via `Drop` implementation

### 4. Memory Management
- Uses `UnsafeCell` for interior mutability pattern
- Implements `Deref` and `DerefMut` for ergonomic access to wrapped data
- Loom-aware construction with `#[cfg]` attributes for testing

## Project Integration
- Used internally by Tokio's runtime components (driver system, synchronization primitives)
- Provides foundation for non-blocking synchronization in async contexts
- Enables safe shared data access in concurrent structures without blocking

## Design Considerations
- Optimized for low-latency access in low-contention scenarios
- SeqCst ordering ensures strict memory visibility guarantees
- PhantomData in guard prevents improper cross-thread sending
- Zero-cost abstraction when lock acquisition succeeds
