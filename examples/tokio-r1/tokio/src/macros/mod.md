# Tokio Macros Module (`macros/mod.rs`)

## Purpose
This file serves as the central hub for macro definitions and conditional compilation of Tokio's async runtime utilities. It organizes various macros used throughout the Tokio ecosystem and enables feature-based inclusion of functionality.

## Key Components

### 1. Core Macro Modules
- **Conditional Compilation**: Uses `cfg_attr` to allow unused macros when `full` feature isn't enabled
- **Fundamental Macros**:
  - `cfg`: Feature flag handling
  - `loom`: Concurrency testing utilities
  - `pin`: Pin projection macros
  - `thread_local`: Thread-local storage
  - `addr_of`: Memory address operations

### 2. Feature-Gated Macros
```rust
cfg_trace! { /* tracing macros */ }
cfg_macros! { /* async primitives */ }
```
- **Tracing**: `trace` module included when tracing is enabled
- **Async Constructs**:
  - `select`: Async operation selection
  - `join`/`try_join`: Concurrent task execution

### 3. Support Infrastructure
```rust
#[doc(hidden)]
pub mod support;
```
Contains internal implementation details for macro support, hidden from public documentation.

## Integration with Project
- **Feature Flag System**: Coordinates with Tokio's configuration system (`cfg!` macros) to enable:
  - Tracing instrumentation
  - Async primitives
  - Filesystem operations
  - Process management
- **Cross-Module Support**: Provides essential macros used by:
  - Async runtime (tasks, context)
  - Networking stack
  - File I/O operations
  - Concurrency primitives

## Conditional Compilation Strategy
Uses custom configuration macros (`cfg_*`) to:
1. Exclude unused code from final binary
2. Enable feature-specific functionality
3. Support different execution environments (WASM, Unix, etc.)
