# Tokio Macros Crate (`tokio-macros/src/lib.rs`)

## Purpose
This file implements procedural macros for Tokio's async runtime, providing developer-friendly attributes to configure and execute async functions. It serves as the foundation for Tokio's attribute macros like `#[tokio::main]` and `#[tokio::test]`, abstracting runtime setup complexity.

## Key Components

### 1. Attribute Macros
- **`#[tokio::main]`**: Transforms async `main` functions into runtime-managed entry points
  - Supports runtime configuration via parameters:
  ```rust
  #[tokio::main(flavor = "multi_thread", worker_threads = 4)]
  ```
  - Generates equivalent runtime builder code
- **`#[tokio::test]`**: Enables async test execution
  - Creates isolated test environments with configurable runtime
- **`main_rt`/`test_rt`**: Lower-level variants for advanced use cases

### 2. Error Handling
- **`main_fail`/`test_fail`**: Provide clear errors when required features are missing
- Validates feature compatibility (e.g., `rt-multi-thread` for multi-threaded runtime)

### 3. Runtime Configuration Support
- Handles multiple runtime flavors:
  - `multi_thread` (default)
  - `current_thread`
- Supports advanced options:
  - Worker thread count
  - Time pausing (`start_paused`)
  - Panic handling strategies
  - Custom crate names

### 4. Implementation Modules
- **`entry`**: Core logic for macro expansions
- **`select`**: Internal implementation of Tokio's `select!` macro

## Integration with Tokio
1. **Runtime Abstraction**: Translates macro parameters to `runtime::Builder` configurations
2. **Async Execution**: Generates boilerplate code for:
   ```rust
   runtime.block_on(async { ... })
   ```
3. **Feature Flag Support**: Integrates with Tokio's feature system (e.g., `test-util` for time control)

## Example Transformation
Input:
```rust
#[tokio::main]
async fn main() {
    println!("Hello Tokio");
}
```

Generated Code:
```rust
fn main() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(async {
            println!("Hello Tokio");
        })
}
```

## Key Design Considerations
- **Developer Experience**: Simplifies async entry points while allowing customization
- **Performance**: Encourages runtime reuse through macro-generated optimal setups
- **Forward Compatibility**: Handles unstable features with `#[cfg(tokio_unstable)]` checks
- **Documentation**: Extensive examples showing macro usage vs equivalent manual code
