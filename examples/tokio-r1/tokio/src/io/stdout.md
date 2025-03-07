# Tokio `stdout.rs` Explanation

## Purpose
This file provides an asynchronous interface to the standard output stream (`stdout`) for the Tokio runtime. It enables non-blocking writes to stdout in a platform-agnostic manner while handling Windows-specific UTF-8 boundary edge cases.

## Key Components

### 1. `Stdout` Struct
- **Composition**: Wraps a `SplitByUtf8BoundaryIfWindows<Blocking<std::io::Stdout>>`
- **Features**:
  - Uses `Blocking` to adapt synchronous I/O for async contexts (likely via thread pool)
  - `SplitByUtf8BoundaryIfWindows` ensures UTF-8 validity on Windows consoles
- **Thread Safety**: Designed for concurrent writes but warns about interleaving with `write_all`

### 2. Platform-Specific Implementations
- **Unix**: Implements `AsRawFd`/`AsFd` for file descriptor access
- **Windows**: Implements `AsRawHandle`/`AsHandle` for handle-based operations

### 3. AsyncWrite Implementation
Delegates to inner components with three core operations:
```rust
fn poll_write(...)  // Non-blocking write
fn poll_flush(...)  // Buffer flush
fn poll_shutdown(...) // Clean shutdown
```

### 4. Constructor
- `pub fn stdout()`: Safely creates an async-ready stdout handle using:
  - `Blocking` wrapper for async compatibility
  - UTF-8 boundary splitter for Windows safety

## Integration with Tokio
- Part of Tokio's I/O module ecosystem
- Complements similar implementations for stderr/stdin
- Works with other utilities like `AsyncWriteExt` for ergonomic usage
- Follows Tokio's pattern of platform-specific optimizations

## Usage Examples
Shown in documentation comments:
```rust
// Basic usage
let mut stdout = io::stdout();
stdout.write_all(b"Hello world!").await?;

// Loop usage pattern
let mut stdout = io::stdout();
for msg in messages {
    stdout.write_all(msg.as_bytes()).await?;
}
```

## Safety Considerations
- Emphasizes single-instance usage in loops to prevent output interleaving
- Contains unsafe block in constructor with justification about buffer safety
- Windows-specific UTF-8 handling prevents partial character writes

---
