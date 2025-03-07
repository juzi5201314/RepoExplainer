### Code File Explanation: `support.rs`

**Purpose:**  
This file provides essential utilities and re-exports for Tokio's procedural macros and async runtime integration. It centralizes commonly used async primitives and runtime-specific functions needed by macros to generate code efficiently.

**Key Components:**

1. **Conditional Imports (`cfg_macros!`):**
   - `maybe_done`: A future utility from Tokio's internals, likely used to handle partial future completion in macro-generated code.
   - `poll_fn`: Re-exported from `std::future` to simplify creating futures from poll functions in macros.
   - `thread_rng_n`: An internal runtime function for thread-local random number generation (used in cooperative scheduling to prevent task starvation).

2. **Re-Exports:**
   - Core async types: `Future`, `IntoFuture`, `Pin`, and `Poll` from `std` are re-exported to ensure they are in scope for macro-generated code, avoiding explicit user imports.

3. **Runtime Integration:**
   - The `thread_rng_n` function delegates to `crate::runtime::context`, linking macros to Tokio's runtime internals for scheduling-related logic.

**Project Context:**
- Works with Tokio's macros (e.g., `#[tokio::main]`, `select!`) to generate boilerplate async code.
- Ensures macros have access to runtime features (e.g., task scheduling, async primitives) while abstracting internal details.
- Examples in related context show how macros rely on these utilities to implement future polling, task spawning, and async control flow.

**Role in the Project:**  