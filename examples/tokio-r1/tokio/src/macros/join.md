# Explanation of `tokio/src/macros/join.rs`

## Purpose
This file defines the `join!` macro, a core concurrency primitive in Tokio. It enables awaiting multiple asynchronous expressions concurrently within a single task, returning when **all** futures complete. This macro is critical for writing efficient, non-blocking async code that multiplexes futures on the same task.

---

## Key Components

### 1. **Documentation Generation (`doc!` macro)**
- The `doc!` macro injects comprehensive documentation into the `join!` macro, including usage examples, runtime characteristics, and comparisons to `try_join!`.
- Highlights that `join!` runs futures **concurrently** (not in parallel) and explains error-handling behavior.

### 2. **Macro Implementation**
- **Conditional Compilation**:
  - `#[cfg(doc)]`: Provides a simplified placeholder for documentation.
  - `#[cfg(not(doc))]`: Contains the actual implementation.
- **Core Logic**:
  - **Normalization Rules**: Recursively processes input futures to generate code for each branch.
  - **Polling Mechanism**:
    - Uses `poll_fn` to create a future that polls all input futures in a round-robin order.
    - Tracks completion with `maybe_done`, ensuring futures are not moved (via `Pin::new_unchecked`).
    - Skips futures in subsequent iterations to prevent starvation.
  - **Output Extraction**: Collects results from completed futures once all are ready.

### 3. **Concurrency Strategy**
- Futures are stored inline (no `Vec` allocation) and polled cooperatively.
- Avoids parallelism by design; for parallelism, users must spawn tasks explicitly via `tokio::spawn`.

---

## Integration with the Project
- **Complement to `try_join!`**: While `join!` waits for all branches regardless of errors, `try_join!` (defined elsewhere) short-circuits on the first error.
- **Task Management**: Integrates with Tokio's task system (e.g., `JoinHandle`, `JoinSet`) for advanced use cases.
- **Runtime Agnostic**: Works with Tokio's single-threaded and multi-threaded runtimes, relying on cooperative scheduling.

---

## Example Usage
```rust
let (result1, result2) = tokio::join!(async_op1(), async_op2());
```
This concurrently runs `async_op1` and `async_op2`, returning a tuple of their results once both complete.

---

## Role in the Project