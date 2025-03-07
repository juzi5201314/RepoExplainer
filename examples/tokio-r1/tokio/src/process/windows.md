# Windows Asynchronous Process Handling in Tokio

## Purpose
This module provides asynchronous process management for Windows in Tokio, enabling non-blocking spawning, waiting, and I/O handling of child processes. It integrates with Windows-specific APIs to monitor process exits and manage standard I/O streams asynchronously.

## Key Components

### `Child` Struct
- **Wraps `std::process::Child`**: Adds async capabilities to the standard child process.
- **`waiting` Field**: Manages asynchronous waiting via a oneshot channel and Windows wait registration.
- **Implements `Future`**: Uses `RegisterWaitForSingleObject` to wait for process exit in a non-blocking manner, completing when the process exits.

### Asynchronous Waiting Mechanism
- **Windows API Integration**: Uses `RegisterWaitForSingleObject` to register a callback in a system thread pool. On process exit, the callback triggers a oneshot sender to notify the async task.
- **Drop Safety**: The `Waiting` struct's `Drop` implementation ensures unregistration of waits to prevent resource leaks.

### I/O Handling (`ChildStdio`)
- **Async Adapters**: Wraps `std::fs::File` handles with `AsyncRead`/`AsyncWrite` implementations using `Blocking` (Tokio's thread-pool executor).
- **Handle Duplication**: Safely duplicates handles for stdio streams using Windows APIs to avoid ownership issues.

### Utilities
- **`spawn_child` Function**: Configures and spawns a child process, converting stdio handles to async-compatible types.
- **Handle Conversion**: Functions like `convert_to_file` and `duplicate_handle` ensure proper handle management across async/await boundaries.

## Integration with Tokio
- **Non-Blocking Process Monitoring**: Fits into Tokio's event loop by deferring blocking operations (like process waiting) to Windows-managed threads.
- **Async I/O Integration**: Bridges synchronous stdio operations to async using Tokio's `Blocking` wrapper, allowing seamless use in async contexts.
- **Orphan Process Handling**: Part of Tokio's broader process management system, ensuring child processes are reaped even if dropped.

## Role in the Project