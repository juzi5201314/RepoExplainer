# Tokio's `parking_lot` Adapter Module

## Purpose
This module provides a thin wrapper around `parking_lot` synchronization primitives to mimic the interface of Rust's standard library (`std::sync`) types. It ensures compatibility with Tokio's concurrency requirements while leveraging `parking_lot`'s performance benefits. The primary goal is to maintain the same API as `std::sync` while preventing unintended `Send` trait implementations that could arise from `parking_lot`'s features.

## Key Components

### Wrapper Structs
- **`Mutex<T>`**, **`RwLock<T>`**, **`Condvar`**:  
  Thin wrappers around `parking_lot` equivalents, with `PhantomData` markers to enforce `std::sync`-compatible type semantics.
- **Guard Types** (`MutexGuard`, `RwLockReadGuard`, `RwLockWriteGuard`):  
  Proxy types for `parking_lot` guards, ensuring dereference operations and `Send`/`Sync` traits match `std::sync` behavior.

### Critical Features
1. **PhantomData Usage**:  
   Ensures the compiler treats these types as if they were `std::sync` primitives, preventing `parking_lot`-specific features (like `send_guard`) from affecting Tokio's concurrency guarantees.
2. **API Mirroring**:  
   Methods like `lock()`, `try_lock()`, `wait()`, and `notify_one()` replicate `std::sync` functionality while delegating to `parking_lot` internally.
3. **Condition Variable Handling**:  
   `Condvar` methods adapt `parking_lot`'s API to return `std::sync`-style `LockResult` and `WaitTimeoutResult`.

### Conditional Compilation
- Uses `#[cfg(not(all(loom, test)))]` to enable `const_new` in non-test environments, ensuring compatibility with Tokio's loom testing framework.

## Integration with the Project
- **Performance Optimization**: Replaces `std::sync` primitives with faster `parking_lot` implementations in Tokio's runtime.
- **Concurrency Safety**: Maintains Tokio's strict `Send`/`Sync` requirements by aligning guard types with `std::sync` semantics.
- **Extensibility**: Designed to be extended with additional methods (e.g., `is_poisoned`, `into_inner`) as needed.

## Example Usage
```rust
// Tokio's Mutex internally uses the wrapped parking_lot type
let mutex = Mutex::new(42);
let guard = mutex.lock();
println!("Value: {}", *guard);
```

## Role in the Project