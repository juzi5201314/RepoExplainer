# Tokio TCP Owned Split Implementation

## Purpose
This module provides owned split functionality for `TcpStream`, allowing it to be divided into two independently owned halves: `OwnedReadHalf` (for asynchronous reading) and `OwnedWriteHalf` (for asynchronous writing). This enables concurrent read/write operations without lifetime constraints, using `Arc` for shared ownership.

## Key Components

### 1. Core Structs
- **`OwnedReadHalf`**: 
  - Wraps an `Arc<TcpStream>` for read operations.
  - Implements `AsyncRead` with methods like `poll_read`, `poll_peek`, and `try_read`.
  - Provides stream metadata access (e.g., `peer_addr`, `local_addr`).

- **`OwnedWriteHalf`**:
  - Wraps an `Arc<TcpStream>` with a `shutdown_on_drop` flag.
  - Implements `AsyncWrite` with methods like `poll_write` and automatic shutdown on drop.
  - Includes write utilities like `try_write` and stream metadata.

### 2. Splitting/Reuniting
- **`split_owned(stream)`**:
  - Splits a `TcpStream` into owned read/write halves using `Arc` for shared ownership.
- **`reunite()`**:
  - Validates halves belong to the same stream via `Arc::ptr_eq`.
  - Recovers the original `TcpStream` if valid, otherwise returns `ReuniteError`.

### 3. Error Handling
- **`ReuniteError`**:
  - Indicates invalid reunification attempts (halves from different streams).
  - Implements `Error` and `Display` for clear error reporting.

### 4. Async Traits
- **`AsyncRead` for `OwnedReadHalf`**:
  - Delegates to `TcpStream`'s internal `poll_read_priv`.
- **`AsyncWrite` for `OwnedWriteHalf`**:
  - Delegates to `TcpStream`'s `poll_write_priv` and handles shutdown logic.

## Key Features
- **Zero-Cost Abstraction**: No runtime overhead compared to generic splits.
- **Ownership Safety**: Uses `Arc` to manage shared stream access without lifetimes.
- **Automatic Shutdown**: `OwnedWriteHalf` closes the write side on drop unless disabled via `forget()`.
- **Concurrency Ready**: Halves can be moved across tasks/threads freely.

## Integration with Project
- Part of Tokio's networking utilities, complementing borrowed splits (`split()`).
- Enables efficient concurrent I/O patterns (e.g., separate read/write tasks).
- Integrates with Tokio's async ecosystem via `AsyncRead`/`AsyncWrite` traits.

---
