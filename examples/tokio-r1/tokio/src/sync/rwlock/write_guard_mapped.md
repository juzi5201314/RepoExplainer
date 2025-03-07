# Tokio RwLockMappedWriteGuard Implementation

## Purpose
This file implements `RwLockMappedWriteGuard`, a specialized RAII guard for write access to a mapped portion of data protected by Tokio's `RwLock`. It enables safe, scoped write access to subcomponents of locked data while preventing dangerous operations like guard downgrading.

## Key Components

### Core Struct
- `RwLockMappedWriteGuard<'a, T: ?Sized>`: Main guard type containing:
  - Semaphore reference for lock management
  - Pointer to mapped data
  - Permit tracking for proper lock release
  - Tracing support for diagnostics
  - PhantomData for lifetime/ownership tracking

### Important Methods
1. **`map()`**  
   Transforms the guard to focus on a subcomponent using a projection closure, creating a new mapped guard.

2. **`try_map()`**  
   Conditional version of `map()` that preserves the original guard if projection fails.

3. **`skip_drop()`**  
   Internal method to safely transfer ownership during mapping while avoiding double-free.

### Trait Implementations
- `Deref`/`DerefMut`: Enable direct access to guarded data
- `Drop`: Releases semaphore permits when guard goes out of scope
- `Debug`/`Display`: Delegates to underlying data's implementations

### Safety Features
- Prevents guard downgrading through type separation
- Uses `ManuallyDrop` and pointer operations for safe memory management
- Maintains semaphore permit count for proper lock state tracking

## Integration with Project
This type works with Tokio's synchronization primitives to:
1. Enable granular write access to locked data structures
2. Support async-friendly lock management
3. Complement other guard types (`RwLockWriteGuard`, `OwnedRwLockWriteGuard`)
4. Integrate with Tokio's tracing infrastructure for debugging

## Critical Design Choices
- Separate type from base write guard to prevent unsafe downgrade operations
- Mutable projection without additional locking through careful lifetime management
- Conditional tracing support that compiles out in stable releases
