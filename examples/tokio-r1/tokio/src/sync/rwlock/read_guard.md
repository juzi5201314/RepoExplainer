# Tokio RwLockReadGuard Implementation

## Purpose
This file implements the `RwLockReadGuard` type for Tokio's asynchronous `RwLock`, providing safe read access to shared data. It ensures proper lock semantics through RAII (Resource Acquisition Is Initialization), automatically releasing the read lock when the guard drops.

## Key Components

### Core Struct
- `RwLockReadGuard<'a, T: ?Sized>`: RAII guard that maintains a read lock on an `RwLock`
  - Contains a semaphore reference (`s`) for lock management
  - Holds a raw pointer (`data`) to the protected data
  - Uses `PhantomData` for lifetime tracking
  - Includes optional tracing spans for diagnostics

### Important Methods
1. **`map`/`try_map`**:
   - Allow projecting the guard to reference subfields of protected data
   - Enable ergonomic access to nested data without early lock release
   - `try_map` handles fallible projections by returning `Result`

2. **`skip_drop`**:
   - Internal method to transfer ownership without triggering drop logic
   - Used during guard projection operations

### Trait Implementations
- `Deref`: Provides transparent access to protected data
- `Debug`/`Display`: Delegates formatting to the underlying data type
- `Drop`: Releases semaphore permits and updates tracing when guard drops

## Concurrency Management
- Uses a `batch_semaphore::Semaphore` to track read locks
- Releases 1 permit in `Drop` implementation to decrement reader count
- Maintains thread safety through RAII pattern and lifetime enforcement

## Integration with Project
- Part of Tokio's synchronization primitives
- Works with other guard types (`RwLockWriteGuard`, `OwnedRwLockReadGuard`)
- Enables safe shared read access in async contexts
- Integrates with Tokio's tracing system for diagnostic visibility

## Notable Features
- Zero-cost projections via `map`/`try_map`
- Conditional tracing support (enabled via `tokio_unstable` feature)
- Lifetime-bound access to prevent use-after-free
- Clippy annotations for proper drop behavior detection
