# Tokio Process Module (`mod.rs`)

## Purpose
This file implements asynchronous process management for Tokio, providing a `Command` API similar to `std::process::Command` but with non-blocking operations. It enables spawning child processes, managing I/O streams, and handling process lifecycle in an async-compatible way.

## Key Components

### 1. `Command` Struct
- **Functionality**: Wraps `std::process::Command` with async methods (`spawn`, `status`, `output`).
- **Features**:
  - Configures arguments, environment variables, working directory, and stdio handles.
  - Platform-specific extensions (Unix UID/GID, Windows creation flags).
  - `kill_on_drop` option to control child termination on handle drop.

### 2. `Child` Struct
- **Represents**: A spawned child process.
- **Key Methods**:
  - `wait()`: Async wait for process exit.
  - `try_wait()`: Non-blocking status check.
  - `start_kill()`/`kill()`: Process termination.
  - `wait_with_output()`: Collect stdout/stderr after exit.
- **Handles**: Provides access to async stdio streams (`ChildStdin`, `ChildStdout`, `ChildStderr`).

### 3. Async I/O Streams
- **ChildStdin**: Implements `AsyncWrite` for process input.
- **ChildStdout/ChildStderr**: Implement `AsyncRead` for process output/error.
- **Integration**: Convertible to/from standard library stdio types.

### 4. Platform-Specific Logic
- **Unix**: Uses signal handling and process reaping.
- **Windows**: Leverages system APIs for async operations.
- **Abstraction**: Hidden behind `imp` module with OS-specific implementations.

## Key Features
- **Async Process Control**: Non-blocking process spawning and status monitoring.
- **Stdio Management**: Piped I/O streams with Tokio's async I/O traits.
- **Process Groups**: Unix process group management for signal handling.
- **Zombie Prevention**: Best-effort cleanup of exited processes.

## Integration with Tokio
- **Runtime Integration**: Spawned processes are managed by Tokio's event loop.
- **Task Coordination**: Designed to work with `tokio::spawn` for concurrent process management.
- **I/O Integration**: Seamlessly works with `tokio::io` utilities for stream processing.

## Caveats
- **Drop Behavior**: Child processes continue running by default when handles are dropped.
- **Zombie Processes**: Tokio attempts to reap exited processes but provides no strict guarantees.
- **Windows Limitations**: Some Unix features (e.g., process groups) aren't available.

## Example Flow
```rust
let mut child = Command::new("echo")
    .arg("hello")
    .spawn()
    .unwrap();

let status = child.wait().await.unwrap();
```

## Role in Project