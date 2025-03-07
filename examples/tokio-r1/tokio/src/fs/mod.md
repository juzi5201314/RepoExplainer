# Tokio File System Module (`tokio/src/fs/mod.rs`)

## Purpose
This module provides asynchronous file system operations for the Tokio runtime. It bridges blocking file I/O operations with asynchronous execution by offloading tasks to a background thread pool using `spawn_blocking`. It supports common file/directory operations (read, write, metadata, symlinks, etc.) while ensuring compatibility with Tokio's non-blocking runtime.

## Key Components

### Core Utilities
- **High-level functions**: `read`, `read_to_string`, `write`, `copy`, `rename`, etc., for atomic file operations.
- **Directory operations**: `create_dir`, `read_dir`, `remove_dir`, etc.
- **Metadata utilities**: `metadata`, `symlink_metadata`, `try_exists`.
- **File handling**: The `File` type (async wrapper for `std::fs::File`) with methods like `open`, `create`, and async I/O traits (`AsyncRead`, `AsyncWrite`).

### Platform-Specific Features
- **Unix**: Symlink support via `symlink`.
- **Windows**: Separate `symlink_dir` and `symlink_file` for directory/file symlinks.

### Performance Optimization
- **Batching**: Encourages buffered I/O (e.g., `BufReader`, `BufWriter`) to minimize `spawn_blocking` calls.
- **Tuning**: `File::set_max_buf_size` controls I/O chunk sizes for efficiency.

### Asynchronous Adapter
- **`asyncify` function**: Wraps blocking operations into async tasks, handling errors and thread pool execution.

## Integration with Tokio
- **Thread pool offloading**: Uses `spawn_blocking` to run blocking file operations without stalling the async runtime.
- **Interoperability**: Integrates with Tokio's I/O traits (`AsyncRead`, `AsyncWrite`) and utilities like `BufWriter`.
- **Warnings**: Advises against using this module for special files (e.g., pipes), directing users to specialized types like `AsyncFd`.

## Example Workflows
1. **Reading a file**:
   ```rust
   let contents = tokio::fs::read_to_string("file.txt").await?;
   ```
2. **Streaming large files**:
   ```rust
   let mut file = File::open("large.bin").await?;
   file.read_buf(&mut buffer).await?;
   ```
3. **Buffered writes**:
   ```rust
   let mut writer = BufWriter::new(File::create("out.log").await?);
   writer.write_all(b"data").await?;
   writer.flush().await?;
   ```

## Role in the Project