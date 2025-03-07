# Tokio Loom RwLock Implementation

## Purpose
This file provides a wrapper around `std::sync::RwLock` that removes poisoning semantics from its API. It is part of Tokio's synchronization utilities, designed to simplify error handling in concurrent contexts by ignoring lock poisoning (a mechanism where panics in locked threads mark locks as "poisoned").

## Key Components

### `RwLock<T>` Struct
- **Wrapper Type**: Encapsulates `std::sync::RwLock<T>` but redefines its methods to discard poisoning errors.
- **Non-Poisoning Behavior**: Converts `PoisonError` results into valid guards via `into_inner()`, ensuring callers don't need to handle poisoning explicitly.

### Core Methods
1. **`read()` / `try_read()`**
   - Acquires a read guard, returning it even if the lock was previously poisoned.
   - `try_read()` returns `None` on contention instead of propagating errors.

2. **`write()` / `try_write()`**
   - Acquires a write guard, ignoring poisoning by extracting the inner guard from errors.
   - `try_write()` handles both contention (`WouldBlock`) and poisoning scenarios.

### Implementation Details
- **Error Handling**: All methods convert `PoisonError` into valid guards using `into_inner()`, effectively bypassing poisoning checks.
- **Lightweight Wrappers**: Methods are marked `#[inline]` to minimize runtime overhead.
- **Thread Safety**: Inherits `Send`/`Sync` semantics from the underlying `std::sync::RwLock`.

## Integration with Tokio
- Part of Tokio's synchronization primitives, used in contexts where lock poisoning is undesirable (e.g., async tasks with custom panic handling).
- Complements other guards like `OwnedRwLockReadGuard` and `RwLockMappedWriteGuard` in Tokio's concurrency model.
- Used in `loom` testing (a tool for validating concurrent code) to simulate or verify lock behavior without poisoning overhead.

## Role in the Project