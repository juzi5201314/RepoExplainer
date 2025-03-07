# Tokio Loom Mutex Implementation

## Purpose
This file provides a wrapper around `std::sync::Mutex` that removes poisoning semantics from its API. It is designed for use in Tokio's Loom concurrency testing framework to simplify lock handling in scenarios where poisoning (due to thread panics) is not a concern.

## Key Components

### `Mutex<T>` Struct
- A thin wrapper (`pub(crate) struct Mutex<T: ?Sized>(sync::Mutex<T>)`) around the standard library's mutex
- Uses `?Sized` bound to support dynamically sized types
- Removes poisoning error handling from API surface

### Core Methods
1. **Lock Acquisition**
   - `lock()`: Returns `MutexGuard` directly, unwrapping poison errors
   - `try_lock()`: Returns `Option<MutexGuard>`, converting poison errors to valid guards
   - Both methods use pattern matching to handle `Poisoned`/`WouldBlock` cases

2. **Construction**
   - `new()` and `const_new()`: Create new mutex instances
   - Supports both runtime and compile-time initialization

3. **Mutable Access**
   - `get_mut()`: Provides direct mutable access to inner data, ignoring poisoning

### Safety Traits
- Implements `Send` and `Sync` where appropriate
- Maintains thread safety guarantees through trait bounds (`T: Send`)

## Integration with Project
This implementation serves as a concurrency primitive for Loom's testing environment:
1. Simplifies error handling by eliminating poisoning checks
2. Provides deterministic behavior required for concurrency testing
3. Integrates with Loom's simulated thread scheduler
4. Used internally by other synchronization primitives in the framework

## Design Choices
- **Poisoning Removal**: Avoids the extra error-handling complexity for test scenarios
- **Zero-Cost Abstraction**: Maintains performance through `#[inline]` attributes
- **API Compatibility**: Mirrors standard mutex API while altering error semantics
