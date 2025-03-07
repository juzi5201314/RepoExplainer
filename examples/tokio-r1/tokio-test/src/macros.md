# `tokio-test/src/macros.rs` Explanation

## Purpose
This file provides essential assertion macros for testing asynchronous code using Tokio and futures. It simplifies validation of `Poll` states, `Result` outcomes, and timing behavior in async operations.

## Key Components

### 1. Poll State Assertions
- **`assert_ready!`**: Verifies a `Poll` is `Ready`, panicking if `Pending`
- **`assert_pending!`** Checks a `Poll` remains `Pending`, panicking if `Ready`
- **`assert_ready_eq!`** Combines ready check with value equality assertion

### 2. Result Handling
- **`assert_ready_ok!`** Ensures `Poll<Result<T,E>>` is `Ready(Ok)`
- **`assert_ready_err!`** Verifies `Poll<Result<T,E>>` is `Ready(Err)`
- **`assert_ok!`/`assert_err!`** For synchronous `Result` validation

### 3. Timing Assertions
- **`assert_elapsed!`** Validates duration with ±1ms tolerance for timer tests

## Design Features
- **Custom Messages**: All macros support formatted panic messages
- **Error Context**: Provides detailed panic information including unexpected values
- **Composition**: Higher-level macros build on base assertions (e.g., `assert_ready_ok` uses `assert_ready`)

## Integration with Tokio Test
- Works with `task::spawn` to test futures in controlled environments
- Complementary to other testing utilities in the crate (mock I/O, streams)
- Essential for writing concise, readable async tests with clear failure diagnostics

## Example Usage Patterns
```rust
// Testing async future completion
let mut fut = task::spawn(async { 42 });
assert_ready_eq!(fut.poll(), 42);

// Testing error conditions
let mut err_fut = task::spawn(async { Err("failure") });
assert_ready_err!(err_fut.poll());

// Testing pending state
let mut pending_fut = task::spawn(future::pending());
assert_pending!(pending_fut.poll());
```

This file provides foundational testing primitives for async Rust code in Tokio ecosystems.  