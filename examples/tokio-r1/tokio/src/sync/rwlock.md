# Tokio RwLock Implementation

## Purpose
This file implements an asynchronous reader-writer lock (`RwLock<T>`) for Tokio, providing:
- Concurrent read access for multiple readers
- Exclusive write access for single writers
- Write-preferring fairness policy to prevent writer starvation
- Async-aware synchronization using semaphores
- Support for both borrowed and owned (Arc-based) guard variants

## Key Components

### Core Structures
- `RwLock<T>`: Main lock structure containing:
  - `Semaphore` for access coordination
  - `UnsafeCell` for protected data
  - Maximum reader count configuration
  - Tracing support for diagnostics

### Guard Types
- `RwLockReadGuard`/`OwnedRwLockReadGuard`: RAII guards for read access
- `RwLockWriteGuard`/`OwnedRwLockWriteGuard`: RAII guards for write access
- Mapped variants for narrowed access to parts of protected data

### Key Features
1. **Fairness Implementation**:
   - Uses FIFO queue in semaphore
   - Write requests get priority over subsequent read requests

2. **Concurrency Control**:
   - Read operations acquire 1 permit
   - Write operations acquire all permits (`mr` = max readers)
   - Semaphore manages both reader/writer synchronization

3. **Async Integration**:
   - `async` methods for non-blocking acquisition
   - `blocking_` variants for sync contexts
   - Task cancellation safety through queue position management

4. **Safety Mechanisms**:
   - Implements `Send`/`Sync` with proper trait bounds
   - PhantomData markers for lifetime tracking
   - UnsafeCell for interior mutability with access control

## Important Methods
- `read()`/`write()`: Async acquisition methods
- `try_read()`/`try_write()`: Non-blocking attempts
- `blocking_read()`/`blocking_write()`: Sync versions
- `get_mut()`: Direct access when uniquely owned
- `into_inner()`: Consume lock to retrieve data

## Project Integration
- Part of Tokio's sync primitives
- Uses batch semaphore implementation internally
- Integrates with Tokio's tracing infrastructure
- Complements other sync types (Mutex, Notify)
- Provides foundation for shared-state concurrency in async systems

## Testing/Validation
- Bounds checking for Send/Sync/Unpin traits
- Loom-based concurrency testing (when enabled)
- Documentation examples demonstrating usage patterns

## Performance Considerations
- Write-preferring policy impacts reader throughput
- Semaphore operations use atomic instructions
- Owned guards enable Arc-based sharing patterns
- Tracing adds conditional overhead

---
