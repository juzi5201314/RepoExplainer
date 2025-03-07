# Tokio Multi-Thread Scheduler Work-Stealing Queue

## Purpose
This file implements a lock-free, concurrent work-stealing queue used in Tokio's multi-threaded scheduler. Its primary role is to enable efficient task distribution among worker threads, allowing idle threads to "steal" tasks from busy threads' queues when they run out of work.

## Key Components

### 1. Core Structures
- **`Local<T>`**: Producer handle for single-threaded task insertion.
- **`Steal<T>`**: Consumer handle for multi-threaded task stealing.
- **`Inner<T>`**: Shared queue state containing:
  - `head`: Atomic long integer tracking real head and stealer's head
  - `tail`: Atomic short integer for producer position
  - `buffer`: Fixed-size array of task slots

### 2. Concurrency Mechanisms
- **Double-width head**: Uses 64-bit (or 32-bit on platforms without atomic u64) to store:
  - LSB: Real head index
  - MSB: Stealer's temporary head during theft
- **Atomic operations**: Implements lock-free synchronization using compare-and-swap (CAS) operations with various memory orderings (AcqRel, Acquire, Release).

### 3. Key Algorithms
- **Task pushing** (`push_back`, `push_back_or_overflow`):
  - Handles normal insertion and overflow scenarios
  - Moves half the queue to global injection queue when full
- **Task stealing** (`steal_into`):
  - Transfers up to half the queue to another worker
  - Uses atomic head updates to prevent race conditions
- **Task popping** (`pop`):
  - Local worker consumes tasks from its own queue

### 4. Configuration
- **Capacity**: 256 tasks normally, reduced to 4 for Loom testing
- **ABA protection**: Uses wider integers (u64/u32) for head/tail indices where available

## Important Implementation Details
- **Memory management**: Uses `UnsafeCell` and `MaybeUninit` for direct buffer access with manual safety guarantees
- **Batch operations**: Steals/transfers tasks in batches for efficiency
- **Overflow handling**: Integrates with global injection queue when local queue overflows
- **Metrics**: Supports unstable metrics tracking through `cfg_unstable_metrics` feature

## Integration with Tokio Runtime
- Part of the multi-threaded scheduler's core infrastructure
- Works with:
  - Global injection queue for overflow handling
  - Worker thread management
  - Statistics tracking (`Stats` struct)
  - Task lifecycle management (`task::Notified`)

## Safety Considerations
- Strict single-producer/multiple-consumer semantics
- Manual memory management with explicit safety comments
- Loom-based concurrency validation (via conditional compilation)
- Atomic ordering guarantees to prevent data races
