# Tokio Oneshot Channel Implementation

## Purpose
This file implements a one-shot channel for asynchronous communication between tasks, allowing a single value to be sent from a `Sender` to a `Receiver`. It's designed for scenarios requiring exactly one message delivery with minimal overhead.

## Key Components

### Core Structures
- **`Sender<T>`**: Non-async handle for sending values. Implements `send()` that immediately succeeds/fails.
- **`Receiver<T>`**: Async `Future` that resolves to `Result<T, RecvError>`. Handles value reception and cancellation.
- **`Inner<T>`**: Shared state between sender/receiver containing:
  - Atomic state flags
  - `UnsafeCell` storage for the value
  - Waker tasks for async notification

### State Management
Uses atomic bitflags to track:
- `RX_TASK_SET`: Receiver task registered
- `VALUE_SENT`: Message successfully sent
- `CLOSED`: Channel closed
- `TX_TASK_SET`: Sender task registered

### Key Features
1. **Thread Safety**: Uses `loom` primitives for concurrency validation
2. **Drop Handling**: Proper cleanup of wakers and values when either end drops
3. **Async Integration**: Implements `Future` for seamless async/await usage
4. **Error Handling**: Clear error variants (`RecvError`, `TryRecvError`)

## Critical Functions
- **`channel()`**: Creates connected sender/receiver pair
- **`send()`**: Non-blocking send with immediate success/failure
- **`poll_recv()`**: Core async logic driving the receiver future
- **`complete()`**: Atomic state transition for value delivery

## Project Role
This implementation provides fundamental single-value communication primitives for Tokio's async ecosystem. It serves as a building block for higher-level synchronization patterns and task coordination in concurrent systems.

---
