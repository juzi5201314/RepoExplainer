# File: `metadata.rs` in Tokio's `fs` Module

## Purpose
This file provides asynchronous filesystem metadata operations for the Tokio runtime. Its primary purpose is to expose non-blocking versions of standard filesystem metadata queries, specifically implementing `metadata()` as an async counterpart to `std::fs::metadata`.

## Key Components

### Core Function
- **`pub async fn metadata(path: impl AsRef<Path>) -> io::Result<Metadata>`**  
  Asynchronously retrieves filesystem metadata for a given path, including file type, permissions, size, and timestamps. This:
  1. Converts the input path to an owned `PathBuf` to avoid lifetime issues
  2. Uses `asyncify()` to offload blocking I/O (`std::fs::metadata`) to a thread pool
  3. Maintains async runtime efficiency by preventing blocking operations on the main executor

### Implementation Details
- **Symbolic Link Handling**: Follows symlinks to inspect target metadata (unlike `symlink_metadata`)
- **Cross-Platform Support**:
  - Uses `stat` on Unix-like systems
  - Uses `GetFileAttributesEx` on Windows
- **Error Handling**: Propagates standard I/O errors for missing files/permissions

## Relationship to Project
This file is part of Tokio's filesystem API surface, following a consistent pattern seen in related context snippets:
- Uses the `asyncify` helper to bridge blocking syscalls with async execution
- Mirrors standard library APIs (`std::fs`) with async/await semantics
- Integrates with other async filesystem operations (e.g., `read_link`, `read_dir`) in the same module

## Design Patterns
- **Ownership Management**: Clones paths before moving them into blocking closures
- **API Consistency**: Maintains identical signatures to stdlib equivalents where possible
- **Documentation Style**: Includes platform-specific behaviors and error conditions mirroring Rust's standard library docs

## Error Conditions
- Permission denied for target path
- Non-existent path
- Filesystem I/O errors (disk failures, etc.)

---
