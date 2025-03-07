# Tokio `OwnedRwLockMappedWriteGuard` Implementation

## Purpose
Provides an owned RAII guard for exclusive write access to a mapped portion of data protected by an `RwLock`. Ensures safe mutation of specific subfields while preventing dangerous operations like guard downgrading.

## Key Components

### 1. Core Struct
```rust
pub struct OwnedRwLockMappedWriteGuard<T: ?Sized, U: ?Sized = T> {
    // Manages tracing spans for diagnostics
    #[cfg(all(tokio_unstable, feature = "tracing"))]
    resource_span: tracing::Span,
    
    // Tracks acquired semaphore permits
    permits_acquired: u32,
    
    // Reference-counted lock pointer
    lock: Arc<RwLock<T>>,
    
    // Pointer to mapped data portion
    data: *mut U,
    
    // Type marker for ownership
    _p: PhantomData<T>,
}
```

### 2. Mapping Functionality
- **`map()`**: Transforms the guard to point to a subfield using a closure
- **`try_map()`**: Fallible version that returns original guard on `None`
- Uses `skip_drop` with `ManuallyDrop` to safely transfer ownership without triggering destructor

### 3. Access Control
- Implements `Deref`/`DerefMut` for transparent access to guarded data
- Automatic lock release via `Drop` implementation:
  ```rust
  fn drop(&mut self) {
      self.lock.s.release(self.permits_acquired as usize);
      // ...tracing updates
  }
  ```

### 4. Safety Features
- Prevents direct access to original lock to avoid unsafe downgrades
- PhantomData ensures proper ownership tracking
- Separate type from non-mapped guards to prevent API misuse

## Integration with Tokio
- Complements `OwnedRwLockWriteGuard` in async synchronization primitives
- Enables efficient partial data access patterns:
  ```rust
  let guard = lock.write_owned().await;
  let mut mapped = OwnedRwLockWriteGuard::map(guard, |f| &mut f.0);
  ```
- Works with Tokio's tracing infrastructure for runtime diagnostics
- Part of hierarchical guard system including read/write/mapped variants

## Role in Project