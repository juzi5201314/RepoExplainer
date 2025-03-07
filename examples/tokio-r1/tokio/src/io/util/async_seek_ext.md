# AsyncSeekExt Trait Implementation

## Purpose
This file provides extension methods for the [`AsyncSeek`] trait in Tokio's async I/O system. It adds utility methods to perform seek operations asynchronously, enabling non-blocking navigation within streams like files or network sockets.

## Key Components

### 1. `AsyncSeekExt` Trait
An extension trait that adds three core methods to any type implementing [`AsyncSeek`]:
- **`seek`**: Creates a future to move the cursor to a specific position
- **`rewind`**: Convenience method to reset position to start (equivalent to `seek(SeekFrom::Start(0))`)
- **`stream_position`**: Gets current position without moving (equivalent to `seek(SeekFrom::Current(0))`)

### 2. Implementation Details
- Uses Tokio's `seek` function internally
- Returns `Seek` futures that implement `Future<Output = io::Result<u64>>`
- Blanket implementation for all `AsyncSeek` types:
  ```rust
  impl<S: AsyncSeek + ?Sized> AsyncSeekExt for S {}
  ```

### 3. Feature Gating
Conditionally compiled with `cfg_io_util!` macro, indicating this is part of Tokio's optional I/O utilities.

## Integration with Project
- Complements Tokio's async I/O primitives (e.g., `AsyncRead`, `AsyncWrite`)
- Used in conjunction with types like `File` and `Cursor` in async contexts
- Enables patterns like:
  ```rust
  file.seek(SeekFrom::Start(6)).await?;
  file.rewind().await?;
  let pos = file.stream_position().await?;
  ```

## Examples
Shown in documentation tests:
1. Seeking in byte buffers
2. File manipulation with position tracking
3. Integration with reading operations

This file provides asynchronous seek operations for Tokio's I/O system, extending base async capabilities with position management utilities.  