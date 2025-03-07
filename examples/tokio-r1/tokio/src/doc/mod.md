# Tokio Documentation Stubs Module (`doc/mod.rs`)

## Purpose
This module serves as a documentation facade for types that are referenced in Tokio's documentation but are either:
- Defined in external crates (e.g., `std`)
- Conditionally compiled types that might not be available in all configurations
- Implementation details hidden from public API

It ensures proper documentation generation on docs.rs while preventing accidental use of placeholder types.

## Key Components

### 1. `NotDefinedHere` Type
```rust
#[derive(Debug)]
pub enum NotDefinedHere {}
```
- **Uninhabited type** (empty enum) that cannot be instantiated
- Used as a documentation placeholder for type aliases
- Prevents accidental misuse through compile-time guarantees
- Implements `mio::event::Source` with no-op methods for feature-gated documentation

### 2. Conditional Implementations
```rust
#[cfg(feature = "net")]
impl mio::event::Source for NotDefinedHere { ... }
```
- Provides dummy implementations for documentation purposes
- Only compiled when `net` feature is enabled
- Ensures trait implementations appear in relevant documentation sections

### 3. OS-Specific Module
```rust
#[cfg(any(feature = "net", feature = "fs"))]
pub mod os;
```
- Contains platform-specific documentation stubs
- Conditionally compiled based on network/filesystem features
- Likely documents cross-platform I/O types using `NotDefinedHere` pattern

## Documentation Strategy
- Uses Rust's `ignore` attribute in code examples to prevent compilation attempts
- Creates type aliases pointing to standard library types with custom documentation:
  ```rust
  /// See [std::os::windows::io::RawSocket]
  pub type RawSocket = crate::doc::NotDefinedHere;
  ```
- Maintains documentation consistency across feature flags
- Leverages Rust's type system to enforce documentation integrity

## Project Role
This module acts as a documentation scaffolding system, enabling:
- Cross-referencing of external types in Tokio's docs
- Feature-gated documentation generation
- Type safety in documentation examples
- Clean separation between actual implementation and documentation artifacts
