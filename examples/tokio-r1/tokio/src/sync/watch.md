# Tokio Watch Channel Implementation

## Purpose
This file implements a multi-producer, multi-consumer channel that retains only the last sent value. It's designed for scenarios where multiple components need to watch for updates to a shared value (e.g., configuration changes). Receivers track the last seen version and efficiently wait for new updates.

## Key Components

### Core Structures
- **`Sender<T>`**: Broadcasts values to all connected receivers. Clones share the same underlying state.
- **`Receiver<T>`**: Observes values and asynchronously waits for changes. Each receiver independently tracks seen versions.
- **`Shared<T>`**: Internal shared state containing:
  - `RwLock<T>`: Stores the current value with read/write access
  - `AtomicState`: Tracks version and closed status using bitwise operations
  - Reference counters for senders/receivers
  - Notification mechanisms (`BigNotify` for receivers, `Notify` for sender closure)

### Key Mechanisms
1. **Version Tracking**:
   - Uses atomic operations to manage a version counter
   - Lowest bit tracks closed state, remaining bits track version
   - Incremented on every value change

2. **Change Detection**:
   - Receivers compare their stored version with the shared state
   - `borrow()` provides unvalidated access, `borrow_and_update()` marks as seen

3. **Efficient Notifications**:
   - `BigNotify` uses multiple `Notify` instances to reduce contention
   - Random/circular selection of notifiers spreads wakeup patterns

4. **Thread Safety**:
   - Atomic operations and `loom`-aware synchronization primitives
   - RwLock ensures safe concurrent access to the stored value

### Important Methods
- **`channel()`**: Creates sender/receiver pair with initial value
- **`Receiver::changed()`**: Async wait for new versions
- **`Sender::send()`**: Broadcast new value (fails if no receivers)
- **`Sender::send_modify()`**: In-place mutation with automatic notification
- **`Sender::subscribe()`**: Creates new receiver even after closure

## Integration with Project
This implementation is part of Tokio's synchronization primitives. It integrates with:
- Task scheduling via async `changed()` notifications
- Cooperative cancellation through Tokio's runtime
- Loom model checking for concurrency safety verification

## Design Considerations
- **Memory Efficiency**: Only stores latest value, no history
- **Backpressure Handling**: No backpressure - new values overwrite old ones
- **Concurrency Model**: Optimized for read-heavy workloads with RwLock
- **Closed State Handling**: Automatic detection when all receivers drop

## Safety Features
- Atomic reference counting for shared state cleanup
- Panic safety in mutation closures
- Thread-safe operations verified through Loom tests
