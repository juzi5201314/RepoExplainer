# Tokio RwLockWriteGuard Implementation

## Purpose
This file implements the `RwLockWriteGuard` structure, a key synchronization primitive in Tokio's async RwLock implementation. It provides exclusive write access to protected data while ensuring proper lock management through RAII (Resource Acquisition Is Initialization) patterns.

## Key Components

### Core Structure
- `RwLockWriteGuard`: RAII guard that releases exclusive write access when dropped
- Contains:
  - Semaphore reference for permit management
  - Pointer to protected data
  - Permit tracking (permits_acquired)
  - Tracing support for diagnostics
  - PhantomData for lifetime tracking

### Major Functionality
1. **Lock Management**:
   - Automatically releases permits on drop via `Drop` impl
   - Uses semaphore operations for async-aware locking

2. **Guard Transformations**:
   - `map()`: Creates mapped write guard for subfields
   - `downgrade()`: Converts to read guard atomically
   - `try_map()`: Fallible version of map
   - `into_mapped()`: Converts to mapped write guard

3. **Safety Mechanisms**:
   - `ManuallyDrop` pattern in `skip_drop()` for safe state transfer
   - Phantom type markers for lifetime correctness
   - #[clippy::has_significant_drop] to warn about improper handling

### Integration Points
- Works with `RwLockMappedWriteGuard` for partial data access
- Coordinates with `RwLockReadGuard` for downgrade operations
- Built on Tokio's batch semaphore implementation
- Integrates with tracing for async task monitoring

## Critical Implementation Details
- **Permit Management**: Write guards hold all permits (prevents concurrent access)
- **Zero-cost Conversions**: Uses pointer manipulation for guard type changes
- **Thread Safety**: Leverages Rust's ownership system rather than atomic operations
- **Tracing Integration**: Conditional compilation for performance-sensitive contexts

## Project Role
This file is central to Tokio's write-side locking mechanism in its RwLock implementation, ensuring safe exclusive access to shared data in asynchronous contexts while enabling flexible guard transformations and proper resource cleanup.
