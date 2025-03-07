# Tokio Ctrl-C Signal Handler

## Purpose
This file provides a cross-platform asynchronous API to listen for Ctrl-C signals in Tokio applications. It abstracts OS-specific signal handling implementations (Unix vs Windows) while ensuring consistent behavior across platforms.

## Key Components

### Platform Abstraction
- Uses conditional compilation (`#[cfg(unix)]`/`#[cfg(windows)]`) to select OS-specific implementations
- Delegates to `os_impl` module (Unix or Windows backend)
- Exposes unified `ctrl_c()` async function interface

### Core Functionality
- `ctrl_c()` async function:
  - Returns `io::Result<()>`
  - Registers a listener on first poll/await
  - Completes when first Ctrl-C is received after registration
  - Uses platform-specific implementations through `os_impl::ctrl_c()`

### Important Caveats
- **Unix Behavior Change**: First registration permanently overrides default SIGINT handling
- **Process-wide Impact**: Signal handling persists even after dropping the listener
- **Non-resetting Behavior**: Default OS behavior not restored after listener termination

## Integration with Project
- Part of Tokio's signal handling system (`tokio::signal` module)
- Works with other OS-specific signal types (Ctrl-Break, Ctrl-Close on Windows)
- Uses Tokio's async runtime for non-blocking signal processing
- Complements other signal types (e.g., SIGHUP handling in Unix)

## Example Usage Patterns
1. Blocking main thread until Ctrl-C:
```rust
signal::ctrl_c().await.expect("Failed to listen");
```

2. Background listener:
```rust
tokio::spawn(async {
    signal::ctrl_c().await.unwrap();
    // Handle cleanup
});
```
