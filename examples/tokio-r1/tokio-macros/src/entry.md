# Tokio Macros Entry Point (`entry.rs`)

## Purpose
This file implements the procedural macros `#[tokio::main]` and `#[tokio::test]` that handle runtime configuration and async function execution. It provides attribute-based runtime configuration for Tokio applications and tests.

## Key Components

### 1. Runtime Configuration Enums
- **`RuntimeFlavor`**: Determines execution model (`current_thread` or `multi_thread`)
- **`UnhandledPanic`**: Defines panic handling strategies (`ignore` or `shutdown_runtime`)
- **`FinalConfig`**: Aggregates validated runtime settings
- **`Configuration`**: Processes and validates macro attributes

### 2. Attribute Parsing
- Handles macro attributes like `flavor`, `worker_threads`, and `start_paused`
- Validates attribute combinations and values
- Maintains backward compatibility with deprecated names

### 3. Code Generation
- **`parse_knobs`**: Transforms async functions into runtime-executed code
- Generates appropriate runtime builder code based on configuration
- Handles special cases for test functions

### 4. Macro Entry Points
- **`main`**: Processes `#[tokio::main]` attributes
- **`test`**: Handles `#[tokio::test]` attributes with test-specific logic

## Key Functionality
- Validates and processes macro attributes
- Generates runtime initialization code
- Transforms async functions into runtime-executed code
- Handles error reporting with helpful diagnostics
- Maintains IDE compatibility through error recovery

## Integration with Project
- Part of `tokio-macros` crate
- Works with Tokio's runtime system (`runtime` module)
- Integrates with Tokio feature flags (e.g., `rt-multi-thread`)
- Complements other Tokio macros and utilities

## Important Implementation Details
- Custom function parsing with `ItemFn` structure
- Span-aware error reporting
- Attribute validation hierarchy
- Runtime builder code generation
- Test function special handling (future pinning)
