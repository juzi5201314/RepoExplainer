# Unix Child Process Handling in Tokio

## Purpose
This module provides Unix-specific implementations for managing child processes asynchronously in Tokio. It handles process lifecycle events (like exits), I/O operations, and orphan process reaping while integrating with Tokio's event loop.

## Key Components

### 1. Signal-Based Process Tracking
- Uses `SIGCHLD` signals to detect child process exits since Unix lacks direct epoll integration for processes.
- Implements a `Signal` stream (from `tokio-net`) to monitor signals and trigger status checks.

### 2. Orphan Process Management
- **`GlobalOrphanQueue`**: Singleton queue for tracking orphaned processes to prevent zombies.
  - Uses conditional compilation for different mutex initialization strategies (`cfg_has_const_mutex_new`).
  - Implements `OrphanQueue` trait to push/reap orphans during signal handling.

### 3. Child Process Reapers
- **`Reaper`**: Generic reaper that checks process status on `SIGCHLD` notifications.
- **`PidfdReaper`** (Linux-only): Uses `pidfd` API for more efficient process tracking when available.
- Enum `Child` wraps different reaper implementations:
  ```rust
  pub(crate) enum Child {
      SignalReaper(Reaper<...>),
      #[cfg(...)]
      PidfdReaper(...)
  }
  ```

### 4. Async I/O Handling
- **`Pipe`/`ChildStdio`**: Wraps file descriptors for child process I/O:
  - Sets non-blocking mode using `fcntl`
  - Integrates with `PollEvented` for async read/write operations
  - Implements `AsyncRead`/`AsyncWrite` for Tokio integration

### 5. Process Spawning
- `spawn_child` function:
  - Creates standard child process
  - Configures I/O pipes
  - Attempts pidfd reaper first on Linux, falls back to signal reaper
  - Returns `SpawnedChild` with async handles

## Critical Functionality

### Future Implementation
- `Child` implements `Future` to async-await exit status:
  ```rust
  impl Future for Child {
      type Output = io::Result<ExitStatus>;
      // Polls underlying reaper implementation
  }
  ```

### Cross-Platform Abstraction
- Provides uniform interface through:
  - `Kill` trait for process termination
  - Standard I/O conversion methods (`convert_to_stdio`)
  - Consistent error handling across Unix variants

### Zombie Prevention
- Automatic orphan reaping during:
  - Signal handling
  - `GlobalOrphanQueue` operations
  - Process drop handlers

## Integration with Tokio
- Leverages Tokio's signal handling system
- Integrates with runtime via `PollEvented` for I/O readiness
- Participates in async task scheduling through `Future` impl

---
