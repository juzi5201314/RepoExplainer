# Tokio Directory Builder (`dir_builder.rs`)

## Purpose
This file implements an asynchronous directory builder for Tokio, providing a non-blocking interface to create directories with configurable options. It mirrors [`std::fs::DirBuilder`](https://doc.rust-lang.org/std/fs/struct.DirBuilder.html) but adapts it for async execution within the Tokio runtime.

## Key Components

### 1. `DirBuilder` Struct
- **Fields**:
  - `recursive: bool`: Controls whether parent directories are created automatically (default: `false`).
  - `mode: Option<u32>` (Unix-only): Sets Unix permissions for new directories (e.g., `0o755`).

### 2. Core Methods
- **`new()`**: Initializes a builder with default settings (non-recursive, default permissions).
- **`recursive()`**: Configures recursive directory creation.
- **`create(path)`**: Asynchronously creates a directory at the specified path using the configured options. Delegates to `std::fs::DirBuilder` via [`asyncify`](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html) to avoid blocking the async runtime.

### 3. Unix-Specific Features
- **`mode()`**: Allows setting directory permissions (e.g., `0o775`) on Unix-like systems using [`DirBuilderExt`](https://doc.rust-lang.org/std/os/unix/fs/trait.DirBuilderExt.html).

## Integration with Tokio
- Part of Tokio's filesystem utilities (`tokio::fs`), complementing functions like `create_dir_all`.
- Enables fine-grained control over directory creation (recursiveness, permissions) in async contexts.
- Uses Tokio's `asyncify` to offload blocking filesystem operations to a dedicated thread pool.

## Example Usage
```rust
DirBuilder::new()
    .recursive(true)
    .mode(0o750) // Unix-only
    .create("/tmp/a/b/c")
    .await?;
```

## Error Handling
Propagates errors from the underlying filesystem operations, including:
- Existing file/directory conflicts
- Permission issues
- I/O errors during creation

## Relationship to Other Code
- Complements `create_dir_all` (simpler recursive creation with defaults).
- Extends Tokio's filesystem API to match `std::fs` capabilities with async ergonomics.

---
