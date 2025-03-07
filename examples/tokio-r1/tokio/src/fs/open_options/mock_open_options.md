# Mock OpenOptions Implementation for Tokio FS Testing

## Purpose
This file provides a mock implementation of `std::fs::OpenOptions` for testing asynchronous file operations in Tokio. It enables controlled testing without real filesystem interactions by simulating file opening behaviors.

## Key Components

### Mock Structure
- **`Mock! { ... }` macro**: Generates a mock version of `OpenOptions` using `mockall` crate
- Core methods mirror standard APIs:
  - File configuration: `append()`, `create()`, `read()`, `write()`, `truncate()`
  - File opening: `open<P: AsRef<Path>>` returning `MockFile`
  - Builder pattern methods returning `&mut Self`

### Platform-Specific Extensions
- **Unix**: Implements `OpenOptionsExt` with `custom_flags()` and `mode()`
- **Windows**: Implements Windows-specific `OpenOptionsExt` including:
  - `access_mode()`
  - `share_mode()`
  - `security_qos_flags()`

### Cloning Support
- Implements `Clone` trait to match real `OpenOptions` behavior

## Testing Integration
- Conditionally compiled with `#[cfg(test)]`
- Replaces standard implementation in tests via:
  ```rust
  #[cfg(test)]
  use mock_open_options::MockOpenOptions as StdOpenOptions;
  ```
- Maintains identical API surface to real implementation for seamless substitution

## Relationship to Project
- Part of Tokio's filesystem testing infrastructure
- Works with `MockFile` to enable isolated unit tests
- Allows validation of file operation configurations without I/O overhead
