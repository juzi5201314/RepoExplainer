### Purpose
This file provides an asynchronous implementation of `symlink_metadata` for Tokio's filesystem operations. It allows non-blocking querying of metadata for symbolic links (without following them), mirroring [`std::fs::symlink_metadata`](https://doc.rust-lang.org/std/fs/fn.symlink_metadata.html) in an async-compatible manner.

### Key Components
1. **Async Wrapper**:  
   The `symlink_metadata` function wraps the blocking `std::fs::symlink_metadata` using Tokio's `asyncify` utility. This offloads the filesystem operation to a blocking thread pool, preventing it from stalling the async runtime.

2. **Path Handling**:  
   Converts the input path to an owned `PathBuf` (`path.as_ref().to_owned()`) to ensure thread safety when moving the path into the async closure.

3. **Error Propagation**:  
   Returns `io::Result<Metadata>`, propagating filesystem errors (e.g., permission issues, invalid paths) through Tokio's async error handling.

### Integration with the Project
- Part of Tokio's `fs` module, which provides async replacements for synchronous `std::fs` operations.
- Follows a consistent pattern seen in related context (e.g., `read_link`, `metadata`, `create_dir`), where blocking operations are delegated to `asyncify`.
- Enables async/await workflows for filesystem tasks in Tokio applications, such as inspecting symbolic links without blocking the event loop.

### Role in the Project