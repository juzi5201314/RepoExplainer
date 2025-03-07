# Tokio Bidirectional Copy Utility

## Purpose
This module provides asynchronous bidirectional data copying between two streams (`AsyncRead + AsyncWrite`). It enables simultaneous data transfer in both directions while handling proper stream shutdown and buffer management.

## Key Components

### 1. Transfer State Management
- **`TransferState` enum**: Tracks progress through three phases:
  - `Running`: Active data copying with a `CopyBuffer`
  - `ShuttingDown`: Flushing remaining data and shutting down the writer
  - `Done`: Final state with byte count

### 2. Core Algorithm
- **`transfer_one_direction`**: State machine that:
  1. Copies data using buffer while streams are active
  2. Initiates graceful shutdown when EOF detected
  3. Tracks total bytes transferred

### 3. Bidirectional Implementation
- **`copy_bidirectional_impl`**:
  - Uses two independent `TransferState` instances (A→B and B→A)
  - Leverages `poll_fn` to create async future
  - Concurrently progresses both directions using Tokio's cooperative scheduling

### 4. Buffer Management
- Default 8KB buffers via `copy_bidirectional()`
- Customizable buffer sizes through `copy_bidirectional_with_sizes()`
- Utilizes `CopyBuffer` from parent module for efficient data transfer

## Key Features
- Zero-copy optimization through buffer reuse
- Proper stream shutdown handling
- Concurrent bidirectional transfer
- Error propagation from either stream
- Graceful EOF handling in either direction

## Integration with Project
Part of Tokio's I/O utilities (`io-util` feature), this implementation:
- Builds on `AsyncRead`/`AsyncWrite` traits
- Reuses buffer logic from `copy` module
- Complements unidirectional copy utilities
- Used for proxy-like scenarios requiring full duplex communication
