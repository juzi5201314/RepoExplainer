markup
### Purpose
This file implements the asynchronous seek operation as a `Future` for Tokio's I/O module. It provides non-blocking cursor positioning functionality for async I/O resources.

### Key Components
1. **`Seek` Future Struct**:
   - Represents an ongoing seek operation
   - Contains:
     - Mutable reference to an `AsyncSeek` implementer
     - Optional `SeekFrom` position
     - `PhantomPinned` to enforce pinning semantics

2. **`seek` Constructor Function**:
   - Creates a new `Seek` future
   - Initializes with target position and pinned marker

3. **Future Implementation**:
   - `poll` method handles state transitions:
     1. Checks for existing seek operations using `poll_complete`
     2. Initiates new seek with `start_seek` when clear
     3. Tracks operation completion through state machine
   - Handles both pending and ready states
   - Manages error propagation

### Integration with Project
- Part of Tokio's async I/O system
- Implements `AsyncSeekExt::seek` method functionality
- Follows pattern used by other async I/O operations (read/write)
- Works with Tokio's runtime for cooperative task scheduling
- Ensures proper pinning for async safety with I/O resources

### Key Patterns
- State machine pattern for async operation progression
- Pinning mechanics for safe async operations
- Error handling integration with `io::Result`
- Separation between operation initiation and completion polling
