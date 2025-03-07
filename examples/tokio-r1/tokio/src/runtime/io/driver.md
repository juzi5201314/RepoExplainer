# Tokio I/O Driver Implementation

## Purpose
This file implements the core I/O event driver for Tokio's runtime, leveraging Mio for system-level event polling. It manages I/O resource registration, event processing, and readiness notification to asynchronous tasks.

## Key Components

### 1. Core Structures
- **`Driver`**: Main event loop handling:
  - Mio polling (`mio::Poll`)
  - Event processing
  - Signal readiness tracking
  - Contains `mio::Events` for event storage

- **`Handle`**: Shared reference to driver capabilities:
  - Manages registrations via `RegistrationSet`
  - Provides synchronization through `Mutex<Synced>`
  - Contains wake mechanism (except on WASI)
  - Tracks metrics (file descriptors, ready events)

### 2. Registration Management
- **`RegistrationSet`**: Tracks all registered I/O resources
- **`ScheduledIo`**: Per-resource state container
- Thread-safe operations using `loom` synchronization primitives

### 3. Event Processing
- **`turn()` method**: Core event loop:
  1. Polls Mio with optional timeout
  2. Processes wake/signal tokens
  3. Dispatches I/O readiness to `ScheduledIo` instances
  4. Updates metrics

### 4. Readiness System
- **`Ready`**: Bitflags representing I/O states
- **`Direction`**: Read/Write operation tracking
- **`Tick`**: Versioning system to prevent stale readiness notifications

### 5. Platform Adaptations
- Conditional compilation for:
  - Signal handling (Unix-only)
  - Waker support (disabled on WASI)
  - Network components (Unix-specific extensions)

## Integration with Project
- Part of Tokio's runtime driver system
- Collaborates with:
  - **Signal handling** (separate module)
  - **Time driver** (through handle structure)
  - **Task scheduler** (via wake notifications)
- Metrics integration for runtime observability

## Critical Operations
1. **Resource Registration** (`add_source()`):
   - Allocates `ScheduledIo`
   - Registers with Mio's registry
   - Updates FD metrics

2. **Event Dispatching**:
   - Converts Mio events to Tokio's `Ready` states
   - Atomic updates to resource readiness
   - Task wakeup via `ScheduledIo::wake()`

3. **Shutdown Handling**:
   - Cleans up registrations
   - Propagates shutdown state to all I/O resources

## Concurrency Model
- Uses lock-free patterns where possible
- `Mutex` protects shared registration state
- Atomic operations on `ScheduledIo` readiness
- Thread-safe handle sharing (enforced via `_assert_kinds`)

---
