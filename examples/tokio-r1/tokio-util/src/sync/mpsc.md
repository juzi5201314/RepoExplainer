# PollSender Implementation in Tokio-Util

## Purpose
This file implements `PollSender<T>`, a wrapper around Tokio's MPSC (Multi-Producer Single-Consumer) channel sender that enables polling-based usage. It bridges Tokio's async channels with the `futures::Sink` trait, allowing integration with polling-based systems and manual flow control.

## Key Components

### 1. PollSendError
- Error type for closed channel scenarios
- Carries unsent item (if available)
- Implements `std::error::Error` and display formatting

### 2. State Machine
```rust
enum State<T> {
    Idle(Sender<T>),      // Ready to acquire permit
    Acquiring,            // Waiting for channel capacity
    ReadyToSend(OwnedPermit<T>), // Has reserved slot
    Closed                // Channel closed
}
```

### 3. PollSender Core
- Maintains channel state and permit acquisition future
- Key fields:
  - `sender`: Underlying Tokio channel sender
  - `state`: Current state machine state
  - `acquire`: Reusable future for permit acquisition

### 4. Main Functionality
- **poll_reserve()**: 
  - Async reservation of channel capacity
  - Returns `Poll::Ready` when slot available
- **send_item()**: 
  - Sends value using reserved slot
  - Must be preceded by successful `poll_reserve`
- **Flow Control**:
  - `close()`: Graceful shutdown
  - `abort_send()`: Cancel in-progress send
  - `is_closed()`: Status check

### 5. Sink Trait Implementation
Implements `futures_sink::Sink` with:
- `poll_ready`: Maps to `poll_reserve`
- `start_send`: Maps to `send_item`
- `poll_flush`: Immediate readiness
- `poll_close`: Clean shutdown

## Implementation Details
- Uses `ReusableBoxFuture` for efficient future management
- Handles lifetime complexity with careful unsafe code
- Maintains thread safety through `Send` bounds
- Provides panic safety through `track_caller` attributes

## Integration with Project
- Part of Tokio's utility crate (tokio-util)
- Enables MPSC channels to work with polling-based systems
- Provides backpressure-aware sending mechanism
- Integrates with async ecosystem via Sink trait
