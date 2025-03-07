# Unix Signal Handling in Tokio

This file (`unix.rs`) provides Unix-specific implementations for asynchronous signal handling in the Tokio runtime. It enables listening for OS signals (e.g., `SIGINT`, `SIGTERM`) and converting them into asynchronous streams that integrate with Tokio's event loop.

## Key Components

### 1. **Signal Types & Initialization**
- **`OsStorage`**: A storage structure initialized for all possible Unix signals. It maps signal IDs to `SignalInfo` entries.
- **`OsExtraData`**: Manages a Unix socket pair (`sender`/`receiver`) to notify the runtime when a signal is received.
- **`SignalInfo`**: Tracks signal registration state using `Once` (for one-time initialization) and `AtomicBool` (thread-safe flag).

### 2. **Signal Registration**
- **`signal_enable`**: Registers a signal handler via `signal_hook_registry`, ensuring handler setup occurs once per signal. Forbidden signals (e.g., `SIGKILL`) are blocked.
- **`action`**: The global signal handler that records events and writes to the notification socket to wake the runtime.

### 3. **Public API**
- **`SignalKind`**: Represents Unix signals (e.g., `SIGINT`, `SIGTERM`) with constructors like `interrupt()` and `terminate()`. Converts between raw OS integers and Rust types.
- **`Signal`**: The async listener returned by `signal()`. Uses `RxFuture` to wait for notifications via a `watch::Receiver`.

### 4. **Integration with Tokio Runtime**
- **`globals()`**: Manages shared state (e.g., registered listeners, socket pair).
- **`signal_with_handle`**: Enables signals for a specific runtime handle, returning a channel receiver for notifications.

## How It Works
1. **Signal Handler Setup**: When a `Signal` is created, `signal_enable` registers a handler that writes to a Unix socket upon signal receipt.
2. **Event Notification**: The runtime monitors the socket's read end. When data is written, it triggers async tasks waiting on the signal.
3. **Async Stream**: The `Signal` struct exposes `recv()` and `poll_recv()` to await or poll for signals, integrating with Tokio's async model.

## Key Considerations
- **Coalescing Signals**: Multiple signals may be merged into a single notification.
- **Permanent Handlers**: Once registered, signal handlers persist for the process lifetime.
- **Thread Safety**: Uses atomic operations and `Once` for safe initialization.

## Example Usage
```rust
use tokio::signal::unix::{signal, SignalKind};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut sig = signal(SignalKind::interrupt())?;
    sig.recv().await; // Blocks until SIGINT (Ctrl+C) is received
    println!("Received SIGINT");
    Ok(())
}
```

## Role in the Project