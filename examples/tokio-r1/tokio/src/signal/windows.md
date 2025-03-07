# Windows Signal Handling Module

## Purpose
This module provides Windows-specific implementations for handling system signals like CTRL-C, CTRL-BREAK, and system events (logoff/shutdown/close). It enables asynchronous monitoring of these events using Tokio's runtime, translating native Windows console control handlers into streamable futures.

## Key Components

### 1. Signal Listeners
- **CtrlC**: Listens for CTRL-C (interrupt) signals
- **CtrlBreak**: Listens for CTRL-BREAK signals
- **CtrlClose**: Listens for window close events
- **CtrlShutdown**: Listens for system shutdown events
- **CtrlLogoff**: Listens for user logoff events

### 2. Core Structures
- `RxFuture`: Internal future type from Tokio's signal system
- Platform-specific implementation in `windows/sys.rs` (real) and `windows/stub.rs` (docs)

### 3. Key Functions
- `ctrl_c()`, `ctrl_break()`, etc.: Factory functions creating signal listeners
- `recv()`: Async method to wait for next signal
- `poll_recv()`: Non-async polling method for manual future implementations

### 4. Implementation Details
- Uses Windows API `SetConsoleCtrlHandler` internally
- Coalesces rapid successive events to prevent overflow
- Broadcasts notifications to all active listeners

## Integration with Project
- Part of Tokio's cross-platform signal handling system
- Complements Unix signal implementations in other modules
- Enables Windows applications to gracefully handle system events in async workflows
- Integrates with Tokio's runtime through future-based API

## Example Usage
```rust
let mut ctrl_c = ctrl_c()?;
ctrl_c.recv().await;
println!("Received CTRL-C");
```

## Design Considerations
- `#[must_use]` annotations prevent unused listeners
- Coalescing prevents missed notifications from event storms
- Stub implementations enable documentation generation on Unix
- Ergonomic API matches Tokio's async patterns
