# Code Explanation: `tokio/src/process/unix/reap.rs`

## Purpose
This file defines the `Reaper` struct, a core component for managing asynchronous child process reaping in Tokio's Unix process handling. Its primary responsibilities include:
- Monitoring child process exits via signals (e.g., `SIGCHLD`).
- Coordinating between polling for process completion and signal-driven notifications.
- Ensuring orphaned processes are tracked and reaped to prevent zombies.

## Key Components

### 1. **`Reaper` Struct**
- **Generics**:
  - `W: Wait`: Represents a child process that can be waited on.
  - `Q: OrphanQueue<W>`: Manages orphaned processes not yet reaped.
  - `S: InternalStream`: Stream for signal notifications (e.g., `SIGCHLD`).
- **Fields**:
  - `inner: Option<W>`: The child process being monitored.
  - `orphan_queue: Q`: Queue for orphaned processes.
  - `signal: S`: Signal stream for process exit notifications.

### 2. **Core Functionality**
- **Future Implementation**:
  - The `poll` method checks for process completion using `try_wait()`.
  - Registers interest in the next signal (`SIGCHLD`) before polling to avoid deadlocks.
  - Returns `Poll::Pending` if the process hasn't exited, ensuring the task is notified on new signals.
- **Orphan Handling**:
  - On drop, if the child hasn't exited, it is moved to the `orphan_queue` for later reaping.
- **Kill Support**:
  - Delegates to the inner `Kill` implementation to terminate the child process.

### 3. **Integration with Tokio**
- **Signal-Driven Workflow**:
  - Uses `InternalStream` (e.g., a signal listener) to efficiently wait for process exits without busy polling.
- **Orphan Queue**:
  - Part of Tokio's global orphan management system, ensuring no zombie processes are left behind.

### 4. **Testing**
- **Mock Components**:
  - `MockWait`, `MockStream`, and `MockQueue` simulate process waiting, signal delivery, and orphan tracking.
- **Test Scenarios**:
  - Validate pending state transitions, successful exits, kill operations, and orphan queuing on drop.

## Relationship to Project
- **Process Lifecycle Management**:
  - The `Reaper` is used in Tokio's `Child` future (e.g., `Child::SignalReaper`) to asynchronously wait for process completion.
  - Integrates with Tokio's signal handling and runtime to avoid blocking threads.
- **Preventing Zombies**:
  - Works with `OrphanQueue` to ensure all child processes are reaped, even if their `Reaper` is dropped before completion.

---
