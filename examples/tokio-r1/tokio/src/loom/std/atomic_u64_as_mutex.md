# Tokio Loom AtomicU64 Mutex Implementation

## Purpose
This file provides a mutex-based implementation of atomic u64 operations for use in Tokio's Loom testing environment. It enables deterministic concurrency testing by replacing hardware atomic operations with mutex-guarded operations that Loom can instrument and analyze.

## Key Components

### Conditional Module Selection
```rust
cfg_has_const_mutex_new! { /* ... */ }
cfg_not_has_const_mutex_new! { /* ... */ }
```
- Selects between two implementations based on const Mutex constructor availability
- Uses `atomic_u64_static_const_new.rs` when const constructors are available
- Falls back to `atomic_u64_static_once_cell.rs` with OnceCell for older Rust versions

### AtomicU64 Structure
```rust
pub(crate) struct AtomicU64 {
    inner: Mutex<u64>,
}
```
- Wraps a u64 value in a Mutex to simulate atomic operations
- Provides thread-safe access through mutex locking

### Atomic Operation Implementations
Implements core atomic operations using mutex locks:
- `load`: Lock and read value
- `store`: Lock and write value
- `fetch_add`: Atomic add with return of previous value
- `fetch_or`: Atomic bitwise OR with return of previous value
- `compare_exchange`: Compare-and-swap operation
- `compare_exchange_weak`: Same as compare_exchange (no spurious failures)

### StaticAtomicU64 Integration
```rust
pub(crate) use static_macro::StaticAtomicU64;
```
- Provides a static version of AtomicU64 through conditional compilation
- Supports different initialization strategies based on environment capabilities

## Project Context
- Part of Tokio's Loom concurrency testing framework
- Enables predictable execution ordering for concurrency analysis
- Used in components requiring atomic u64 operations during testing:
  - Scheduler state management
  - Resource tracking
  - Concurrency primitive implementations
- Integrates with other Loom components like `OnceCell`, `RwLock`, and various atomic types

## Design Considerations
- Mimics std::sync::atomic::AtomicU64 API surface
- Prioritizes correctness over performance for testing purposes
- Allows Loom to explore all possible thread interleavings
- Provides consistent behavior across Rust versions through conditional compilation
