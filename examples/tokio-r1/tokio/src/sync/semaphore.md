# Tokio Semaphore Implementation

## Purpose
This file implements an asynchronous counting semaphore for the Tokio runtime. It controls concurrent access to shared resources by managing a limited number of permits. Key features include:
- Fair permit distribution using FIFO queuing
- Support for bulk permit acquisition
- Both borrowed and owned permit variants
- Thread-safe implementation using atomic operations
- Integration with Tokio's tracing infrastructure

## Key Components

### 1. Semaphore Struct
```rust
pub struct Semaphore {
    ll_sem: ll::Semaphore, // Low-level implementation
    #[cfg(tracing)]
    resource_span: tracing::Span,
}
```
- Wraps a low-level semaphore implementation
- Contains tracing instrumentation for debugging
- Maintains permit count and wait queue

### 2. Permit Types
- **`SemaphorePermit`**: Borrowed permit tied to semaphore lifetime
- **`OwnedSemaphorePermit`**: Arc-wrapped permit for cross-task usage

### 3. Core Functionality
- **Permit Acquisition**:
  - `acquire()`/`acquire_many()`: Async methods for permit acquisition
  - `try_acquire()`: Non-blocking attempt
  - `acquire_owned()`: For moving permits between tasks
- **Permit Management**:
  - `add_permits()`: Dynamically adjust available permits
  - `close()`: Prevent new acquisitions
  - `available_permits()`: Check current capacity

### 4. Advanced Features
- Permit merging/splitting
- Rate limiting examples
- Test synchronization patterns
- Token bucket implementation

## Implementation Details

### Fairness Guarantee
Uses an internal waitlist (linked list) to ensure:
- First-come-first-served permit allocation
- Fair treatment of bulk and single acquisitions
- Prevention of starvation

### Performance Considerations
- Atomic operations for permit counting
- Async/await integration with Tokio scheduler
- Zero-cost abstractions for permit management

## Usage Examples
The code provides extensive documentation examples for:
1. File handle limiting
2. Request concurrency control
3. Test serialization
4. Rate limiting patterns
5. Database connection pooling

## Integration with Tokio
- Works with Tokio's async task system
- Supports `Arc` for shared ownership
- Implements proper drop semantics for automatic permit release
- Integrates with Tokio's tracing system when enabled

## Safety & Correctness
- Thread-safe through atomic operations
- Proper panic handling in constructors
- Loom model testing annotations
- Clear ownership semantics for permits
