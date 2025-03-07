# Tokio Task ID Module

## Purpose
This module defines the `Id` type, which provides unique identifiers for tasks within the Tokio runtime. These IDs are used to track and reference tasks during their execution, enabling debugging, task management, and runtime introspection.

## Key Components

### `Id` Struct
- **Opaque Identifier**: Wraps a `NonZeroU64` to ensure uniqueness and non-zero values for optimization.
- **Properties**:
  - Unique relative to *currently running* tasks (reusable after task completion).
  - Non-sequential and unrelated to task spawn order or runtime context.
- **Derived Traits**: `Clone`, `Copy`, `Debug`, `Hash`, `Eq`, `PartialEq` for usability in collections and comparisons.

### ID Generation
- **Static Atomic Counter**: Uses `NEXT_ID` (an atomic `u64`) to generate new IDs thread-safely.
- **Loom Support**: Conditional compilation for concurrency testing with Tokio's `loom` tool.
- **Loop Handling**: Ensures non-zero values even if the counter overflows (unlikely with `u64`).

### Public Functions
- `id()`: Returns the current task's ID or panics if called outside a task context.
- `try_id()`: Returns `Option<Id>`, safe for non-task contexts.

### Utility Methods
- `as_u64()`: Exposes the raw numeric ID.
- `Display` implementation: Allows formatting IDs for logging/diagnostics.

## Integration with the Project
- **Runtime Context**: Used via `context::current_task_id()` to fetch IDs from task-local storage.
- **Task APIs**: Integrated with `JoinHandle::id()`, task spawning, and debugging tools like `Handle::dump`.
- **Concurrency Safety**: Leverages atomic operations and `loom` for thread-safe ID generation.

## Related Context
- Referenced in task spawning, blocking operations, and runtime diagnostics.
- Used in task dumps for snapshotting runtime state (e.g., `tokio_unstable` features).

---

This file provides the foundational mechanism for uniquely identifying and tracking tasks in Tokio's asynchronous runtime.  