# Task-Local Storage Implementation in Tokio

## Purpose
This file implements task-local storage for Tokio's async runtime, providing a mechanism to store data that is scoped to the lifetime of a task or async block. Unlike thread-local storage, task-local values are tied to async task execution contexts rather than OS threads.

## Key Components

### 1. `task_local!` Macro
- Declares static variables that become task-local keys
- Generates `LocalKey` instances with thread-local storage backing
- Supports multiple declarations with preserved visibility and attributes
- Example usage:
  ```rust
  task_local! {
      pub static LOG_TRACE_ID: String;
      static DB_CONN: Connection;
  }
  ```

### 2. `LocalKey` Struct
- Core type representing a task-local storage key
- Contains thread-local storage using `RefCell<Option<T>>`
- Key methods:
  - `scope()`: Sets value for async block execution
  - `sync_scope()`: Synchronous version for non-async contexts
  - `with()`/`try_with()`: Access current task-local value
  - `get()`: Clone value (requires `Clone` impl)

### 3. `TaskLocalFuture` 
- Pinned future type returned by `LocalKey::scope()`
- Manages value propagation through nested async scopes
- Implements drop guard to clean up task-local values
- Contains safety mechanisms for proper pinning behavior

### 4. Error Handling
- `AccessError`: Indicates missing task-local value
- `ScopeInnerErr`: Handles borrow/access violations during scoping
- Panics with contextual messages for API misuse

## Implementation Details

### Scoping Mechanism
- Uses a stack-based approach for nested scopes
- `scope_inner` manages value swapping with RAII guards
- Thread-local storage with `RefCell` ensures per-task isolation

### Safety Features
- PhantomPinned prevents moving values across await points
- PinnedDrop implementation handles proper cleanup
- Borrow checking through RefCell prevents concurrent access

### Integration with Tokio
- Works with Tokio's task system through Future trait impls
- Leverages thread-local storage while maintaining async safety
- Enables context propagation across async boundaries

## Usage Patterns
Typical use cases include:
- Request tracing IDs in web servers
- Database connection management
- Authentication context propagation
- Distributed tracing spans

Example async usage:
```rust
task_local! { static USER_ID: u32; }

async fn handle_request() {
    USER_ID.scope(42, async {
        let id = USER_ID.get();
        // Perform authenticated operations
    }).await;
}
```

## Project Role