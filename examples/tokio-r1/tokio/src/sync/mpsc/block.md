# Tokio MPSC Channel Block Implementation

## Purpose
This file implements the `Block` structure used in Tokio's multi-producer single-consumer (MPSC) channel. It provides a lock-free, linked list-based storage mechanism for message passing between asynchronous tasks.

## Key Components

### Core Structures
- **`Block<T>`**: 
  - A node in a linked list holding up to `BLOCK_CAP` messages
  - Contains:
    - `header`: Metadata including start index and atomic pointers
    - `values`: Array of message slots using `UnsafeCell` for interior mutability

- **`BlockHeader<T>`**:
  - Tracks block metadata:
    - `start_index`: First slot index in block
    - `next`: Atomic pointer to next block
    - `ready_slots`: Bitmask tracking filled slots
    - `observed_tail_position`: Safety marker for memory reclamation

### Concurrency Control
- **Atomic Operations**:
  - Uses `AtomicPtr` for thread-safe linked list navigation
  - `ready_slots` bitmask (AtomicUsize) tracks message availability
  - Flags: `RELEASED`, `TX_CLOSED` for state transitions

- **Memory Management**:
  - Custom allocation via `Layout` with manual initialization
  - `UnsafeCell` and `MaybeUninit` for safe uninitialized memory handling
  - Atomic reference counting for block lifecycle management

### Critical Operations
1. **Block Creation**:
   - `new()`: Allocates and initializes blocks with proper alignment
   - `initialize()`: Sets up value storage with thread-safe cells

2. **Message Handling**:
   - `write()`: Stores values with proper memory ordering
   - `read()`: Retrieves values using acquire/release semantics
   - `tx_close()`: Signals channel closure to receivers

3. **Block Management**:
   - `grow()`: Expands linked list atomically using CAS operations
   - `tx_release()`: Marks blocks safe for reclamation
   - `reclaim()`: Resets blocks for reuse

## Integration with Project
- Works with `Tx` (transmitter) and `Rx` (receiver) components:
  - Transmitters write to blocks using atomic slot tracking
  - Receivers read messages and manage block lifecycle
- Forms foundation of Tokio's MPSC channel implementation:
  - Enables lock-free message passing between async tasks
  - Supports backpressure through block allocation strategy
- Integrates with Tokio's loom testing framework for concurrency validation

## Safety Considerations
- Manual memory management with `UnsafeCell` and raw pointers
- Strict adherence to atomic operation ordering (Acquire/Release)
- Thread-local data access patterns verified through loom
