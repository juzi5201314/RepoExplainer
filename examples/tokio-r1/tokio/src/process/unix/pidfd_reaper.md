# Tokio PIDFD Reaper Implementation

## Purpose
This module provides an asynchronous mechanism for reaping child processes on Linux using the `pidfd` API. It integrates with Tokio's event loop to efficiently wait for process exits without blocking, improving scalability compared to traditional methods.

## Key Components

### 1. `Pidfd` Structure
- **Function**: Wraps a Linux pidfd file descriptor
- **Key Features**:
  - Uses `syscall(SYS_pidfd_open)` to create non-blocking file descriptors
  - Caches unsupported kernel detection with `AtomicBool`
  - Implements MIO `Source` for event loop integration

### 2. `PidfdReaperInner` Future
- **Responsibility**: Async waiting for process termination
- **Mechanism**:
  - Uses `PollEvented` to monitor pidfd readiness
  - Checks for runtime shutdown errors and re-registers interest
  - Calls `try_wait()` when fd becomes readable

### 3. `PidfdReaper` Public Interface
- **Components**:
  - Optional inner future for pidfd-based waiting
  - Orphan queue fallback mechanism
- **Functionality**:
  - Implements `Deref` for direct child process access
  - Handles process killing through `Kill` trait
  - Manages orphan processes on drop

## Integration Points
- Works with Tokio's orphan process management system
- Falls back to traditional orphan queue when:
  - Kernel lacks pidfd support (<5.10)
  - pidfd creation fails
- Integrates with MIO for async I/O readiness notifications

## Important Implementation Details
- **Atomic Optimization**: Caches pidfd support check to avoid repeated syscalls
- **Error Handling**:
  - Special handling for runtime shutdown errors
  - Proper error propagation through `io::Result`
- **Safety**:
  - Uses `unsafe` blocks responsibly for raw fd handling
  - Maintains proper ownership of file descriptors

## Testing Strategy
- Conditional tests based on kernel version detection
- Verifies:
  - Normal process completion
  - Process killing behavior
  - Orphan process handling
  - Proper cleanup after drops

## Project Role
Provides Linux-specific optimized process management for Tokio using modern kernel features, while maintaining fallback compatibility through orphan queues.
