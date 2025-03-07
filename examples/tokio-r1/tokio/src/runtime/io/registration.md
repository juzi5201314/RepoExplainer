# Tokio I/O Registration Module

## Purpose
The `registration.rs` file provides the `Registration` struct, which associates I/O resources with Tokio's reactor. It enables asynchronous I/O operations by managing event registration, readiness polling, and task notification when I/O events occur.

## Key Components

### `Registration` Struct
- **Handle**: References the runtime scheduler to interact with the I/O driver.
- **Shared State (`Arc<ScheduledIo>`)**: Tracks readiness states and manages task wakers for I/O events.

### Core Functionality
1. **Registration/Deregistration**:
   - `new_with_interest_and_handle()`: Registers I/O resources with the reactor.
   - `deregister()`: Removes I/O resources from reactor tracking.

2. **Readiness Polling**:
   - `poll_read_ready()`/`poll_write_ready()`: Check read/write readiness using Tokio's cooperative scheduling.
   - `poll_ready()`: Core polling logic that interacts with `ScheduledIo` state.

3. **I/O Operations**:
   - `try_io()`: Performs non-blocking I/O, handling `WouldBlock` errors.
   - `async_io()`: Async wrapper for retrying I/O until success.
   - `poll_io()`: Combines readiness polling with I/O operation execution.

4. **Event Management**:
   - `clear_readiness()`: Resets readiness state after processing events.
   - `readiness()`: Async method to wait for specific I/O readiness.

### Safety & Concurrency
- Implements `Send`/`Sync` but requires caller-managed concurrency for polling methods.
- Drop implementation clears wakers to prevent memory leaks from cyclic references.

## Integration with Tokio
- Works with `ScheduledIo` to track I/O states across the runtime.
- Interfaces with the scheduler via `Handle` to access the I/O driver.
- Forms the foundation for higher-level I/O types (TCP sockets, pipes, etc.).

## Critical Design Aspects
- **Dual Readiness Streams**: Separate tracking for read/write operations.
- **Platform Events**: Supports OS-specific readiness notifications via Mio.
- **Cooperative Scheduling**: Integrates with Tokio's task budgeting system.
