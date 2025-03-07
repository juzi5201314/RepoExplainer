# Tokio In-Memory IO Utilities: `mem.rs`

## Purpose
This file provides in-memory asynchronous I/O types (`DuplexStream` and `SimplexStream`) for bidirectional and unidirectional communication, respectively. These act as virtual "pipes" for transferring data between asynchronous tasks without OS-level I/O, useful for testing, mocking, or inter-task communication.

---

## Key Components

### 1. `DuplexStream`
- **Bidirectional Channel**: Created in pairs via `duplex()`, allowing cross-communication (e.g., writing to one end reads from the other).
- **Structure**:
  - `read: Arc<Mutex<SimplexStream>>`: Handles incoming data.
  - `write: Arc<Mutex<SimplexStream>>`: Handles outgoing data.
- **Drop Behavior**: Closing one end notifies the other via `close_write()`/`close_read()`, draining remaining data and returning errors for pending writes.

### 2. `SimplexStream`
- **Unidirectional Channel**: Created via `simplex()` or `new_unsplit()`, supporting split (reader/writer) or unified usage.
- **Core Fields**:
  - `buffer: BytesMut`: Stores data in a growable buffer.
  - `max_buf_size`: Maximum capacity before writes block.
  - `read_waker`/`write_waker`: Task wakeers for pending I/O.
- **Async Methods**:
  - `poll_read_internal()`: Copies data from buffer to `ReadBuf`, waking writers on progress.
  - `poll_write_internal()`: Writes data to buffer, waking readers on new data.
  - Supports vectored writes via `poll_write_vectored_internal()`.

### 3. Concurrency & Coordination
- **Mutex Protection**: Uses `loom::sync::Mutex` for thread-safe access to `SimplexStream` internals.
- **Task Wakeups**: Wakers notify blocked tasks when data becomes available (read) or space frees up (write).
- **Cooperative Scheduling**: Uses `cfg_coop!` macros to integrate with Tokio's task yielding for fairness.

---

## Integration with Tokio
- **Implements Standard Traits**: Both types implement `AsyncRead` and `AsyncWrite`, allowing seamless use with Tokio's I/O ecosystem (e.g., combinators like `copy`, `split`).
- **Interoperability**: Designed to mirror real I/O types (e.g., `TcpStream`, Unix pipes), enabling substitution in tests or pipelines.
- **Utilities**:
  - `duplex()`: Creates linked bidirectional streams.
  - `simplex()`: Creates a unidirectional reader/writer pair.

---

## Example Usage
```rust
let (mut client, mut server) = tokio::io::duplex(64);
client.write_all(b"ping").await?;
server.read_exact(&mut buf).await?; // Receives "ping"
```

---

## Role in the Project