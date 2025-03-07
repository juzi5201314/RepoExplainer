# Mock File Implementation for Tokio FS Testing

## Purpose
This file provides mock implementations of file system operations and async task execution mechanisms for testing purposes in Tokio. It replaces real file I/O with controlled simulations, enabling deterministic testing of asynchronous filesystem operations without actual disk access.

## Key Components

### Mock File Structure
- **`MockFile`**: Simulates `std::fs::File` with mocked methods like `create`, `open`, `read`, `write`, and filesystem operations (`sync_all`, `set_len`).
- **Platform-Specific Traits**: Implements OS-specific traits (`AsRawHandle` for Windows, `AsRawFd` for Unix) to mimic low-level file descriptor/handle access.
- **Inner Methods**: `inner_flush`, `inner_read`, etc., unify method implementations across different reference types (`&mut self` vs `&&self`).

### Trait Implementations
- **`Read`/`Write`/`Seek`**: Implemented for both `MockFile` and `&MockFile` to match `std::fs::File`'s API surface.
- **Async Task Handling**: 
  - `spawn_blocking`/`spawn_mandatory_blocking`: Queue tasks for simulated async execution.
  - `JoinHandle`: Wraps a `oneshot::Receiver` to await mock task results.

### Task Simulation System
- **Thread-Local Queue**: Stores pending tasks in a `VecDeque` using `tokio_thread_local!`.
- **Pool Utilities**: 
  - `pool::len()`: Inspects queue size.
  - `pool::run_one()`: Executes the next queued task, enabling controlled test progression.

## Integration with Project
- **Testing Infrastructure**: Used to validate Tokio's async filesystem operations (read/write, metadata, permissions) without real I/O.
- **Cross-Platform Support**: Mocks OS-specific file interfaces to ensure consistent behavior across Unix/Windows.
- **Determinism**: Allows tests to precisely control task execution order and file operation outcomes.

---
