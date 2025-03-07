# Tokio Configuration Macros (`cfg.rs`)

## Purpose
This file defines a collection of Rust macros for managing conditional compilation (`#[cfg]` attributes) across the Tokio project. It centralizes feature flag checks, platform-specific code handling, and documentation visibility rules to improve maintainability and consistency.

## Key Components

### Core Macros
1. **`feature!` Macro**
   - Base macro for feature-gated code
   - Handles `#[cfg]` attributes and docs.rs documentation
   - Pattern: `#[cfg($meta)]` + `#[cfg_attr(docsrs, doc(cfg($meta)))]`

2. **Platform Macros**
   - `cfg_windows`/`cfg_unix`: OS-specific code with proper docs.rs integration
   - `cfg_unstable_windows`: Combines Windows and Tokio's unstable flag

3. **Feature Flag Macros**
   - `cfg_net`, `cfg_fs`, `cfg_sync`: Gate code behind specific Tokio features
   - `cfg_rt`, `cfg_rt_multi_thread`: Runtime system configuration

4. **Specialized Configuration**
   - `cfg_loom`/`cfg_not_loom`: Loom model checker integration
   - `cfg_taskdump`: Conditional compilation for debugging utilities
   - `cfg_aio`: FreeBSD-specific async I/O support

### Documentation Handling
- Uses `cfg_attr(docsrs, ...)` to maintain accurate documentation on docs.rs
- Shows/hides platform-specific documentation appropriately
- Example: `#[cfg_attr(docsrs, doc(cfg(windows)))]`

### Advanced Combinations
- **Cross-cutting concerns**:
  - `cfg_io_driver`: Combines network, process, and signal features
  - `cfg_coop`: Coordinates cooperative scheduling across multiple features
- **Unstable features**:
  - `cfg_unstable_metrics`: Gates metrics behind `tokio_unstable` flag
  - `cfg_64bit_metrics`: Handles atomic requirements for metrics

## Project Integration
- **Consistent Configuration**: Provides single source of truth for all conditional compilation rules
- **Feature Flag Management**: Enables modular compilation of Tokio components
- **Cross-platform Support**: Abstracts OS differences (Windows/Unix/WASI)
- **Documentation Integrity**: Ensures accurate feature documentation generation
- **Testing Support**: Integrates with Loom for concurrency testing

## Notable Patterns
1. **Documentation Preservation**:
```rust
#[cfg(any(all(doc, docsrs), windows))]  // Include in docs or Windows builds
#[cfg_attr(docsrs, doc(cfg(windows)))]  // Show Windows badge in docs
```

2. **Feature Combinations**:
```rust
#[cfg(any(
    feature = "net",
    all(unix, feature = "process"),
    all(unix, feature = "signal"),
))]
```

3. **Unstable Feature Gating**:
```rust
#[cfg(all(windows, tokio_unstable))]
```
