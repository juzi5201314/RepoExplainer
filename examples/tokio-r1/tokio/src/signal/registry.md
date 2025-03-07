# Code File Explanation: `registry.rs`

## Purpose
This file implements a thread-safe event notification registry system for managing and broadcasting OS signal events to registered listeners in the Tokio runtime. It provides core infrastructure for tracking pending events and distributing notifications efficiently.

## Key Components

### 1. EventInfo
- **Structure**: Contains `pending` (atomic boolean flag) and `tx` (watch channel sender)
- **Role**: Tracks notification state for a specific event ID and provides broadcast capability
- **Default**: Initializes with cleared pending state and new watch channel

### 2. Storage Trait
- **Abstraction**: Defines interface for event storage (`event_info` lookup and `for_each` iteration)
- **Implementation**: Vec<EventInfo> provides basic vector-backed storage

### 3. Registry
- **Generic Structure**: `Registry<S: Storage>` manages event storage and notification logic
- **Core Methods**:
  - `register_listener`: Creates watch channel receiver for event ID
  - `record_event`: Marks event as pending without immediate notification
  - `broadcast`: Sends pending notifications to all listeners atomically

### 4. Globals
- **Singleton Pattern**: Combines OS-specific data (`OsExtraData`) with registry
- **Functionality**:
  - Provides global access point via `globals()` (initialized once using `OnceCell`)
  - Proxies registry methods for listener management
  - Integrates OS-specific storage through `OsStorage`

### 5. Concurrency Mechanisms
- **Atomic Operations**: Uses `AtomicBool` with `Ordering::SeqCst` for thread-safe state management
- **Watch Channels**: Enables efficient broadcast notifications to multiple listeners

## Integration with Project
- **Signal Handling**: Forms foundation for OS signal processing in Tokio
- **Runtime Integration**: Used by signal drivers (e.g., Ctrl+C, process termination)
- **Extensibility**: Generic storage allows platform-specific optimizations through `OsStorage`

## Testing
- **Validation**: Includes tests for:
  - Basic event notification flow
  - Error cases (invalid event IDs)
  - Concurrency scenarios
  - Resource cleanup
- **Runtime Testing**: Uses Tokio's current-thread runtime to verify async behavior

## Role in Project