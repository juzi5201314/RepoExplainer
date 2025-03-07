# Tokio Bounded MPSC Channel Implementation

## Purpose
This file (`bounded.rs`) implements a **bounded multi-producer, single-consumer (MPSC) channel** for asynchronous communication in Tokio. It provides backpressure by blocking senders when the channel's buffer is full, ensuring memory safety and efficient resource utilization.

## Key Components

### 1. Core Structures
- **`Sender<T>`**: Owned handle for sending messages. Clones share the same channel.
- **`Receiver<T>`**: Exclusive receiver for consuming messages.
- **`WeakSender<T>`**: Non-owning sender that doesn't prevent channel closure.
- **Permit Types** (`Permit`, `OwnedPermit`, `PermitIterator`): Manage reserved channel capacity for zero-allocation sends.

### 2. Channel Creation
- **`channel(buffer: usize)`**: Creates a bounded channel with a fixed buffer size. Panics if `buffer == 0`.

### 3. Semaphore Management
- Uses a `batch_semaphore` to track available slots. Each send acquires a permit; receives release permits.

### 4. Key Features
- **Backpressure**: Senders block when buffer is full (via async `send`/`reserve`).
- **Non-blocking Options**: `try_send`, `try_reserve` for immediate attempts.
- **Ownership Control**: `WeakSender` allows detection of channel closure.
- **Batch Operations**: `recv_many`/`poll_recv_many` for bulk message handling.
- **Synchronous Fallbacks**: `blocking_send`/`blocking_recv` for non-async contexts.

## Critical Methods

### Sender
- **`send()`**: Async send with backpressure.
- **`reserve()`**: Reserve capacity before sending (avoids message loss on cancel).
- **`try_send()`**: Immediate send attempt (returns `Err` if full/closed).
- **`downgrade()`**: Converts to `WeakSender`.

### Receiver
- **`recv()`**: Async message reception.
- **`try_recv()`**: Non-blocking receive.
- **`close()`**: Closes channel, preventing new sends.
- **Capacity Tracking**: `capacity()`, `max_capacity()`, `len()`.

### Permits
- **`Permit::send()`**: Uses reserved capacity without allocation.
- **`OwnedPermit`**: Moves sender ownership for static lifetime guarantees.

## Integration with Tokio
- Works with Tokio's runtime for async task scheduling.
- Implements `Stream` via `ReceiverStream` (external wrapper).
- Integrates with Tokio's time features for `send_timeout`.

## Error Handling
- **`SendError`**: Channel closed during send.
- **`TrySendError`**: Immediate failure (closed/full).
- **`TryRecvError`**: No messages available.

## Example Flow
```rust
let (tx, mut rx) = channel(5);
tx.send(1).await.unwrap(); // Uses capacity
let permit = tx.reserve().await.unwrap(); // Reserves slot
permit.send(2);
let msg = rx.recv().await.unwrap();
```

## Role in Project