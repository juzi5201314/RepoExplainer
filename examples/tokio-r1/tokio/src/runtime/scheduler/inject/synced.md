# Tokio Scheduler Injection Queue Synchronization

## Purpose
The `synced.rs` file implements thread-safe synchronization for an injection queue in Tokio's async runtime scheduler. This queue serves as a global task repository where worker threads can steal tasks when their local queues are empty, enabling efficient work distribution across threads.

## Key Components

### `Synced` Struct
```rust
pub(crate) struct Synced {
    pub(super) is_closed: bool,
    pub(super) head: Option<task::RawTask>,
    pub(super) tail: Option<task::RawTask>,
}
```
- **is_closed**: Flag indicating if the queue accepts new tasks
- **head/tail**: Raw pointers forming a linked list of scheduled tasks
- Implements `Send`/`Sync` manually for thread-safe access to unsafe internals

### Core Operations
1. **Task Popping (`pop` method)**:
   - Removes tasks from the queue head using unsafe pointer operations
   - Updates queue linkage while maintaining thread safety
   - Converts raw task pointers into `Notified` tasks ready for execution

2. **State Checking (`is_empty`)**:
   - Simple check for queue emptiness via head presence

## Implementation Details
- Uses raw task pointers (`task::RawTask`) for low-level queue management
- Implements manual memory safety through:
  - Atomic pointer operations
  - Mutable exclusive access (`&mut self`) in critical sections
  - Unsafe blocks for task conversion/pointer manipulation

## Project Context
- Part of Tokio's work-stealing scheduler architecture
- Integrates with:
  - Task lifecycle management (`task::Notified`)
  - Locking mechanisms (`Mutex` in related code)
  - Multi-threaded worker coordination
- Enables cross-thread task injection while maintaining synchronization

## Safety Considerations
- `unsafe` blocks handle:
  - Raw pointer dereferencing
  - Task state transitions
  - Memory ownership transfers
- Manual `Send`/`Sync` implementations ensure proper thread-safety contracts
