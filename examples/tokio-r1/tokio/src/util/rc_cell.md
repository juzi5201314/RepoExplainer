# RcCell in Tokio's Utilities

## Purpose
The `RcCell<T>` struct provides thread-unsafe interior mutability for `Option<Rc<T>>` values. It mimics `Cell<Option<Rc<T>>>` but adds a `get()` method despite `Rc` not being `Copy`, enabling safe cloning of the contained `Rc` without moving ownership.

## Key Components

### Struct Definition
- **`RcCell<T>`**: Wraps an `UnsafeCell<Option<Rc<T>>>` to enable mutable access to an `Rc`-wrapped value in a non-`Sync` context.

### Methods
1. **`new()`**: 
   - Constructs an empty `RcCell` initialized with `None`.
   - Uses conditional compilation (`cfg`) to handle `loom` testing constraints on `UnsafeCell`.

2. **`with_inner()`**:
   - **Safety**: Requires exclusive access (non-recursive, non-concurrent calls).
   - Grants mutable access to the inner `Option<Rc<T>>` via a closure, leveraging `UnsafeCell`'s raw pointer access.

3. **`get()`**:
   - Returns a cloned `Option<Rc<T>>` from the cell. Cloning `Rc` increments its reference count without moving the original.

4. **`replace()`**:
   - Swaps the inner value with a new `Option<Rc<T>>` using `std::mem::replace`, returning the old value.

5. **`set()`**:
   - Updates the cell's value and drops the previous one, ensuring proper cleanup.

## Safety Guarantees
- **Non-`Sync` Design**: Ensures the cell cannot be shared across threads, aligning with `Rc`'s single-threaded nature.
- **Exclusive Access**: `with_inner()` enforces no recursion/concurrency via caller guarantees, preventing data races.

## Integration with Tokio
- Used in single-threaded or non-concurrent parts of Tokio (e.g., task management) where `Rc` is sufficient.
- Complements other utility types like `OnceCell` and `AtomicCell` but avoids atomic overhead for thread-unsafe scenarios.

---
