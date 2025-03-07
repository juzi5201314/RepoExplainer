# Orphan Process Management in Tokio

## Purpose
This file implements an orphan process management system for Unix-based systems in Tokio. Its primary role is to track and "reap" orphaned child processes (zombies) that have exited but haven't been waited on by their parent. This prevents resource leaks and ensures proper process cleanup in asynchronous environments.

## Key Components

### 1. Core Traits
- **`Wait` Trait**: Provides interface for process waiting operations
  - `id()`: Gets process identifier
  - `try_wait()`: Non-blocking check for process exit status
- **`OrphanQueue` Trait**: Defines queue operations for orphan management
  - `push_orphan()`: Adds a process to the orphan queue

### 2. OrphanQueue Implementation
- **`OrphanQueueImpl` Struct**:
  - `sigchild`: Mutex-protected watch channel receiver for SIGCHLD signals
  - `queue`: Mutex-protected vector of orphan processes
  - Implements lazy initialization of SIGCHLD listener
  - Provides thread-safe operations using Tokio's loom synchronization primitives

### 3. Core Functionality
- **`reap_orphans()`**: 
  - Checks for SIGCHLD signals
  - Drains orphan queue when signals are received
  - Efficiently manages process cleanup without blocking
- **`drain_orphan_queue()`**:
  - Iterates through orphan processes in reverse order
  - Removes exited or errored processes
  - Handles EINTR and other system call interruptions gracefully

### 4. Testing Infrastructure
- **`MockQueue`**: Test implementation of OrphanQueue
- **`MockWait`**: Configurable test process simulator
- Comprehensive test cases covering:
  - Queue draining behavior
  - Signal handling scenarios
  - Error condition handling
  - Concurrency edge cases

## Integration with Tokio
- Works with Tokio's signal handling system through `SignalHandle`
- Integrates with process management components via the `Wait` trait
- Collaborates with Tokio's runtime drivers (I/O and Signal) for proper event notification
- Part of Tokio's Unix process management module, complementing process spawning and killing functionality

## Design Considerations
- Lazy initialization of signal listeners to reduce overhead
- Reverse iteration during queue draining for safe element removal
- Thread-safe operations using mutexes from Tokio's loom crate
- Graceful handling of signal driver initialization failures
- Efficient resource management through non-blocking operations
