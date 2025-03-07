# Windows Signal Handling Implementation

## Purpose
This file provides Windows-specific signal handling for console control events (e.g., Ctrl+C, system shutdown) in Tokio's async runtime. It enables asynchronous notification of system events through futures-based APIs.

## Key Components

### 1. Event Handlers
- **Control Event Functions**:  
  `ctrl_break()`, `ctrl_close()`, `ctrl_c()`, `ctrl_logoff()`, `ctrl_shutdown()` create futures (`RxFuture`) that resolve when their respective Windows console events occur.

### 2. Core Mechanism
- **Global Initialization**:  
  `global_init()` sets up a Windows console control handler via `SetConsoleCtrlHandler` using `Once` for thread-safe singleton initialization.
- **Handler Routine**:  
  The `handler` function processes events by:
  - Recording events in global registry
  - Broadcasting to listeners
  - Entering infinite sleep for critical events (close/logoff/shutdown) to prevent process termination

### 3. Event Management
- **OsStorage**:  
  Implements `Storage` trait to manage event state tracking for 5 console events. Maps Windows event IDs to internal `EventInfo` structures.
- **Special Event Handling**:  
  `event_requires_infinite_sleep_in_handler()` identifies events needing special handling to avoid immediate process termination.

### 4. Async Integration
- **RxFuture**:  
  Bridges Windows event notifications to async Rust through a channel-based listener system from `crate::signal::registry`.

### 5. Testing
- **Simulated Events**:  
  Tests use `raise_event` to directly invoke handler logic, bypassing Windows' actual signal delivery mechanism.
- **Runtime Validation**:  
  Tests verify proper future resolution for all event types using Tokio's current-thread runtime.

## Project Integration
- Part of Tokio's cross-platform signal handling system
- Implements Windows-specific components for `tokio::signal` module
- Complements Unix signal handling implementations in other files
- Exposed through public APIs like `tokio::signal::windows::ctrl_c()`

---
