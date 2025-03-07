# Tokio's `OwnedRwLockReadGuard` Implementation

## Purpose
This file defines `OwnedRwLockReadGuard`, an RAII (Resource Acquisition Is Initialization) guard for managing shared read access to Tokio's `RwLock`. It ensures thread-safe read access to shared data and automatically releases the lock when dropped.

## Key Components

### 1. Core Struct
- **`OwnedRwLockReadGuard<T, U>`**: The primary RAII guard containing:
  - `Arc<RwLock<T>>`: Reference-counted pointer to the underlying lock.
  - `*const U`: Raw pointer to the guarded data subset (supports type projection).
  - `PhantomData<T>`: Maintains type ownership semantics.
  - Conditional `tracing::Span`: For diagnostics when `tokio_unstable` and `tracing` features are enabled.

### 2. Key Functionality
- **`map`/`try_map` methods**:
  - Allow projecting the guard to reference nested data components (e.g., struct fields).
  - Use `skip_drop` to safely transfer ownership without triggering premature unlock.
- **`Deref` implementation**:
  - Provides transparent access to guarded data via dereferencing.
- **`rwlock()` method**:
  - Returns a reference to the underlying `Arc<RwLock<T>>` for lock management.

### 3. Drop Semantics
- Releases the read lock via `lock.s.release(1)` in `Drop` implementation.
- Updates tracing metrics when enabled.

### 4. Type Safety
- Uses `mem::ManuallyDrop` and `ptr::read` in `skip_drop` to avoid double-free scenarios during projection.
- Maintains variance relationships through `PhantomData`.

## Integration with Project
- Part of Tokio's synchronization primitives alongside `RwLockWriteGuard` and other variants.
- Enables safe shared read access patterns in async contexts.
- Works with Tokio's tracing infrastructure for runtime diagnostics.
- Supports type-safe data projection patterns seen in other guard types (e.g., `OwnedRwLockWriteGuard`).

## Example Use Case
```rust
let guard = lock.read_owned().await;
let projected_guard = OwnedRwLockReadGuard::map(guard, |data| &data.field);
// Safely access projected field until guard drops
```
