# Tokio Signal Handling in I/O Driver

## Purpose
This file (`signal.rs`) integrates Unix signal handling into Tokio's asynchronous I/O driver. It enables the runtime to process signals (e.g., `SIGINT`, `SIGTERM`) asynchronously via the same event loop used for I/O operations, using a Unix socket pair for signal notification.

## Key Components

### 1. `Handle` Implementation
- **`register_signal_receiver` Method**:
  - Registers a `mio::net::UnixStream` (receiver end of a socket pair) with Tokio's I/O driver registry.
  - Uses `TOKEN_SIGNAL` to uniquely identify signal-related events.
  - Monitors for `READABLE` events to detect incoming signals via the Unix stream.

### 2. `Driver` Implementation
- **`consume_signal_ready` Method**:
  - Checks and resets the `signal_ready` flag, indicating whether a signal event has been received.
  - Used to trigger signal processing in the runtime while preventing redundant handling.

### Supporting Structures
- **`Driver` Struct**:
  - Contains `signal_ready` (flag for pending signals) and `events` (reused `mio::Events` for polling).
- **`Handle` Struct**:
  - Holds a weak reference (`Weak<()>`) to check if the I/O driver is alive before registering handlers.

## Integration with the Project
- **Signal Delivery Mechanism**:
  - Relies on a Unix socket pair. A dedicated thread (outside Tokio) listens for OS signals and writes to the socket, triggering a `READABLE` event on the receiver stream.
- **Event Loop Coordination**:
  - When the I/O driver detects a `READABLE` event with `TOKEN_SIGNAL`, it sets `signal_ready = true`.
  - The runtime periodically checks `consume_signal_ready()` to process pending signals (e.g., notifying registered signal listeners).

## Related Context
- Interacts with `mio` for low-level event polling and Tokio's `PollEvented` for async I/O abstraction.
- Connects to signal registration utilities (`globals`, `EventId`) and async signal streams (`RxFuture`, `Signal`).

---
