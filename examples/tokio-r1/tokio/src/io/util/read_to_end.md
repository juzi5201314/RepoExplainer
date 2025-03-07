markup
# Tokio `read_to_end` Utility Explanation

## Purpose
This file implements an asynchronous `read_to_end` operation for Tokio's I/O module. Its primary purpose is to efficiently read all bytes from an `AsyncRead` source into a buffer until EOF is reached, using adaptive buffering strategies to optimize memory usage and performance.

## Key Components

### 1. `ReadToEnd` Future
- **Structure**: Pinned future containing:
  - Mutable reference to an `AsyncRead`er
  - `VecWithInitialized` wrapper for buffer management
  - Counter for bytes read
  - `PhantomPinned` to ensure !Unpin status
- **Role**: Acts as the asynchronous operation handle, implementing `Future` to drive the reading process

### 2. Core Functions
- **`read_to_end`**: Entry point that initializes the future
- **`read_to_end_internal`**: Main loop handling polling and result aggregation
- **`poll_read_to_end`**: Adaptive reading implementation with:
  - Small buffer (32 bytes) probing for initial reads
  - Direct vector reading after initial capacity
  - Smart capacity management using `VecWithInitialized`

### 3. Adaptive Buffering Strategy
- Uses dual-phase approach:
  1. Initial small read (32 bytes) to detect EOF early
  2. Direct vector reading with exponential growth for large data
- Balances memory efficiency and performance by:
  - Minimizing allocations for small reads
  - Reducing copies through direct vector access
  - Dynamically reserving capacity (minimum 32 bytes per reserve)

## Integration with Tokio
- Part of Tokio's I/O utilities (`tokio::io::util`)
- Complements other async I/O primitives like `read_exact` and `read_until`
- Used by `AsyncReadExt::read_to_end` extension method
- Integrates with Tokio's async runtime through proper `Future`/`Poll` implementation

## Performance Considerations
- Avoids over-allocation through size-adaptive strategy
- Minimizes zero-initialization costs using `MaybeUninit`
- Reduces syscall overhead through buffered reads
- Maintains correctness with `ReadBuf` safety guarantees

## Relationship to Other Components
- Uses `VecWithInitialized` from sibling module for buffer management
- Complements similar utilities like `read_until` and `read_buf`
- Follows patterns seen in other Tokio I/O futures (pin projection, phantom pinned markers)

# Role in Project