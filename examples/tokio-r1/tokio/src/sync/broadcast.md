# Tokio Broadcast Channel Implementation

## Purpose
This file implements a multi-producer, multi-consumer broadcast channel where each sent value is received by all active consumers. It's designed for scenarios requiring efficient message broadcasting to multiple subscribers while handling backpressure and message lag.

## Key Components

### Core Structures
1. **`Sender<T>`**  
   - Cloneable handle for broadcasting values
   - Manages channel state through an `Arc<Shared<T>>`
   - Implements flow control with channel capacity

2. **`Receiver<T>`**  
   - Subscriber handle for receiving values
   - Tracks position in message stream to detect lag
   - Supports resubscription to catch up with current messages

3. **`Shared<T>`**  
   - Central state container with:
     - Circular buffer of `RwLock<Slot<T>>` entries
     - Atomic counters for tracking receivers/senders
     - Mutex-protected tail position and waiters list
   - Implements core broadcast logic and synchronization

4. **`Slot<T>`**  
   - Individual message container with:
     - Remaining receiver count (atomic)
     - Position in sequence
     - Value storage using `UnsafeCell`

### Key Mechanisms
- **Message Propagation**  
  Values are stored once and cloned on demand for receivers
- **Lag Handling**  
  Uses position tracking to detect missed messages (`RecvError::Lagged`)
- **Capacity Management**  
  Evicts oldest messages when capacity exceeded
- **Async Integration**  
  Implements `Future` for async receiving using waiter nodes and wakers
- **Thread Safety**  
  Combines atomic operations (`AtomicUsize`, `AtomicBool`) with mutex/rwlock synchronization

## Critical Functionality

### Message Flow
1. **Sending**  
   - Locks tail position
   - Writes to next buffer slot
   - Updates remaining receiver count
   - Notifies waiting receivers

2. **Receiving**  
   - Checks message positions for lag detection
   - Manages per-receiver cursor (`next`)
   - Handles async waiting through waiter queue
   - Implements message cloning on demand

### Error Handling
- **`SendError`** - When no active receivers
- **`RecvError::Lagged`** - When receiver misses messages
- **`RecvError::Closed`** - When all senders drop

## Integration with Tokio
- Implements async/await pattern through `Recv` future
- Integrates with Tokio's cooperative scheduling via `coop` module
- Works with Tokio's synchronization primitives (Mutex, RwLock)
- Provides cancellation safety for async operations

## Performance Considerations
- Lock-free reads using RWLock on slots
- Batch wakeup of waiters for efficiency
- Power-of-two buffer sizing for fast modulo operations
- Atomic reference counting for shared state

## Example Usage
```rust
let (tx, mut rx1) = broadcast::channel(16);
let mut rx2 = tx.subscribe();

tx.send(10).unwrap();
assert_eq!(rx1.recv().await.unwrap(), 10);
assert_eq!(rx2.recv().await.unwrap(), 10);
```

## Role in Project
Provides a high-performance broadcast channel implementation for the Tokio runtime, enabling efficient one-to-many message distribution with backpressure handling and async/await integration.
