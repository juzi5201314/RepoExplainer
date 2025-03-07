# `once_cell.rs` Explanation

## Purpose
This file implements a thread-safe `OnceCell<T>` type designed for one-time initialization of values. It provides a mechanism to lazily initialize a value on first access and safely share it across threads, ensuring the initialization logic runs exactly once.

## Key Components

### `OnceCell<T>` Struct
- **Fields**:
  - `once: Once`: Ensures initialization occurs exactly once using the standard library's synchronization primitive.
  - `value: UnsafeCell<MaybeUninit<T>>`: Stores the uninitialized/initialized value with interior mutability.

### Thread Safety
- Implements `Send` and `Sync` for `T: Send + Sync`, allowing cross-thread usage.
- Uses `std::sync::Once` to guarantee thread-safe initialization.

### Core Methods
1. **`new()`**:
   - Creates an empty `OnceCell` with uninitialized storage.

2. **`get(init)`**:
   - Returns a reference to the initialized value.
   - Calls `do_init` if uninitialized, using the provided closure `init`.
   - Uses `Once` to ensure thread-safe initialization and panic propagation.

3. **`do_init(init)`** (Cold Path):
   - Performs actual initialization via `call_once()`.
   - Writes the result of `init` to the cell using unsafe pointer operations, protected by `Once`'s synchronization.

4. **Drop Implementation**:
   - Safely deallocates the initialized value using `drop_in_place`.

## Safety Considerations
- Relies on `std::sync::Once` for synchronization guarantees.
- Uses `UnsafeCell` and manual pointer operations with explicit safety reasoning:
  - Exclusive access during initialization via `Once`'s guarantees.
  - No data races due to `Once`'s completion check before accessing initialized data.

## Relationship to Project
- Used throughout Tokio for lazy initialization of global/shared resources (e.g., signal handlers, static configurations).
- Provides a lightweight alternative to `once_cell`/`lazy_static` crates with Tokio-specific optimizations.
- Integrates with other synchronization primitives (seen in related context like `AtomicBool`, `Semaphore`).

## Design Tradeoffs
- Prioritizes minimal overhead for initialized-value access (`inline` on `get()`).
- Separates cold initialization path (`#[cold]` on `do_init`) for optimizer hints.
- Avoids dependencies by reusing `std::sync::Once` instead of custom atomics.

---
