# ReusableBoxFuture in Tokio-Utils

## Purpose
The `ReusableBoxFuture` struct provides a reusable, heap-allocated container for dynamically dispatched futures. Its primary goal is to minimize reallocations when replacing the stored future, improving performance in scenarios where futures are frequently swapped (e.g., async state machines, task scheduling).

## Key Components

### 1. Core Structure
```rust
pub struct ReusableBoxFuture<'a, T> {
    boxed: Pin<Box<dyn Future<Output = T> + Send + 'a>>,
}
```
- Stores a pinned, boxed future with `Send` bound for thread safety
- Generic over output type `T` and lifetime `'a`

### 2. Allocation Optimization
- **`try_set`/`set` methods**: Safely replace the contained future while reusing the existing allocation if:
  - New future has identical memory layout (size/alignment)
  - Type checks pass for `Send` and lifetime bounds
- Uses `reuse_pin_box` helper to handle memory reuse logic

### 3. Critical Methods
- **`poll`**: Delegates to the inner future's polling mechanism
- **`get_pin`**: Provides mutable access to the pinned future
- **`Future` implementation**: Allows direct use as a future

### 4. Safety Mechanisms
- `CallOnDrop` helper ensures proper cleanup even during panics
- Manual memory management with `ManuallyDrop` and raw pointers
- `unsafe impl Sync` justified by pinned access semantics

## Project Integration
Part of Tokio's utility library (`tokio-util`), this component:
- Enables efficient future management in async runtimes
- Reduces allocator pressure in high-performance scenarios
- Serves as building block for higher-level async primitives

## Performance Characteristics
- Zero-allocation replacements when layout matches
- Fallback to reallocation when layouts differ
- Type-erased storage enables dynamic dispatch

---

Provides a memory-efficient container for dynamically typed futures with allocation reuse capabilities.  