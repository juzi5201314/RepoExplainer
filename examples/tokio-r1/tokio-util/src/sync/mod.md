# Tokio-Util Sync Module Explanation

## Purpose
This module provides specialized synchronization primitives that extend Tokio's core async utilities. It focuses on enhancing async concurrency with polling-based interfaces, cancellation support, and reusable components.

## Key Components

### 1. Cancellation Tokens
- **Exported Types**: `CancellationToken`, `WaitForCancellationFuture`
- **Functionality**: Enables cooperative task cancellation through token-based signaling
- **Key Features**:
  - `DropGuard` for automatic cleanup
  - Owned and referenced future variants

### 2. Poll-Oriented Channels
- **Core Type**: `PollSender`
- **Features**:
  - Non-async polling interface for message sending
  - Error handling via `PollSendError`
  - Integration with Tokio's mpsc channels

### 3. Semaphore Management
- **PollSemaphore**:
  - Async-aware permit acquisition
  - Built on Tokio's `Semaphore` with polling support
  - Thread-safe implementation using atomic operations

### 4. Future Optimization
- **ReusableBoxFuture**:
  - Memory-efficient container for futures
  - Avoids repeated allocations in hot paths
  - Used internally by other synchronization components

## Integration with Tokio Ecosystem
- Complements core Tokio sync modules (`mpsc`, `oneshot`, `Mutex`)
- Provides polling alternatives to async/await interfaces
- Works with Tokio's runtime model through proper `Send`/`Sync` implementations
- Extends error handling with domain-specific errors (`TryRecvError`, `AcquireError`)

## Implementation Patterns
- Heavy use of `Pin` and manual `Future` implementations
- Leverages Tokio's internal synchronization primitives (`batch_semaphore`, `notify`)
- Implements zero-cost abstractions where possible
- Maintains compatibility with standard Tokio channels and semaphores

## Key Relationships
- `PollSender` wraps Tokio's `mpsc::Sender` with polling semantics
- `PollSemaphore` enhances `tokio::sync::Semaphore` with direct poll support
- `ReusableBoxFuture` serves as foundational infrastructure for other components
