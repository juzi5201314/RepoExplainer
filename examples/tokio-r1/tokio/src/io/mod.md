# Tokio I/O Module (`tokio/src/io/mod.rs`)

## Purpose
This module serves as the asynchronous counterpart to Rust's `std::io`, providing foundational traits, utilities, and types for non-blocking I/O operations. It enables efficient, scheduler-aware I/O in Tokio's async runtime.

## Key Components

### Core Traits
- **`AsyncRead` & `AsyncWrite`**:  
  Async versions of `std::io::Read`/`Write`. These traits define basic read/write operations that yield to the scheduler when I/O isn't ready, enabling concurrent task execution.
- **`AsyncBufRead`**:  
  Async equivalent of `std::io::BufRead`, supporting buffered reads with methods like `read_line`.
- **`AsyncSeek`**:  
  Enables asynchronous seeking within streams.

### Utilities
- **Extension Traits (`AsyncReadExt`, `AsyncWriteExt`)**:  
  Add utility methods (e.g., `read`, `write`, `flush`) to types implementing `AsyncRead`/`AsyncWrite`.
- **Buffered I/O**:  
  - `BufReader`/`BufWriter`: Reduce system calls via buffering.
  - `split()`/`join()`: Split bidirectional streams into read/write halves.
- **Adapters**:  
  Utilities like `copy`, `empty`, `sink`, and `repeat` for common I/O patterns.

### Platform-Specific Support
- **Unix**: `AsyncFd` for integrating with Unix file descriptors.
- **BSD**: Optional AIO support via `bsd::Aio`.

### Re-exports
- Standard I/O types (`Error`, `Result`, `SeekFrom`) for compatibility.

## Integration with the Project
- **Foundation for Async I/O**:  
  This module underpins Tokio's networking (`TcpStream`), filesystem (`File`), and standard I/O operations.
- **Interoperability**:  
  - Converts between async I/O and streams/sinks (via `tokio-util`).
  - Bridges `futures_io` and Tokio I/O traits.
- **Feature-Gated Components**:  
  Conditional compilation (e.g., `io_util`, `net`) ensures minimal overhead for unused features.

## Example Usage
```rust
use tokio::io::{AsyncReadExt, BufReader};
use tokio::fs::File;

async fn read_file() -> tokio::io::Result<()> {
    let file = File::open("data.txt").await?;
    let mut reader = BufReader::new(file);
    let mut contents = String::new();
    reader.read_to_string(&mut contents).await?;
    Ok(())
}
```

## Role in the Project