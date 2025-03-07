# Tokio MPSC Channel Error Types

This file defines error types used in Tokio's multi-producer single-consumer (MPSC) channels, handling various failure scenarios during message sending and receiving operations.

## Key Components

### 1. `SendError<T>`
- **Purpose**: Indicates a failed send operation due to a closed channel.
- **Characteristics**:
  - Wraps the unsent value (`T`) for potential recovery
  - Implements `Error` trait
  - Displays "channel closed" message
  - Non-exhaustive debug output to hide sensitive data

### 2. `TrySendError<T>`
- **Purpose**: Represents possible outcomes of non-blocking send attempts.
- **Variants**:
  - `Full(T)`: Channel at capacity (non-blocking failure)
  - `Closed(T)`: Channel closed during send
- **Features**:
  - `into_inner()` method to retrieve unsent value
  - Conversion from `SendError` to `Closed` variant
  - Distinct messages for display ("no available capacity" vs "channel closed")

### 3. `TryRecvError`
- **Purpose**: Indicates failed non-blocking receive attempts.
- **Variants**:
  - `Empty`: Channel temporarily empty
  - `Disconnected`: Channel permanently closed
- **Implementation**:
  - Clear display messages differentiate transient vs permanent failures

### 4. `SendTimeoutError<T>` (Conditional)
- **Purpose**: Represents timeout failures in timed send operations (gated by `cfg_time!`).
- **Variants**:
  - `Timeout(T)`: Operation exceeded time limit
  - `Closed(T)`: Channel closed during attempt
- **Features**:
  - Mirror structure to `TrySendError` with timeout-specific handling

### 5. Deprecated `RecvError`
- **Legacy**: Previously used for receive errors, now replaced by `Option` returns
- **Note**: Maintained for backward compatibility but marked as unused

## Design Patterns
- **Value Preservation**: All send errors contain original message for recovery
- **Error Conversion**: Seamless conversion between error types (`SendError` → `TrySendError`)
- **Conditional Compilation**: Timeout-related errors only included when time feature is enabled
- **Ergonomic Display**: Human-readable messages without exposing internal data

## Integration with Project
- Used throughout Tokio's channel implementations (`Sender`, `Receiver`)
- Returned by critical operations:
  - Blocking/non-blocking sends (`send`, `try_send`)
  - Timed sends (`send_timeout`)
  - Non-blocking receives (`try_recv`)
- Forms error handling foundation for Tokio's message passing system
