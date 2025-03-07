### Code Explanation: `unconstrained.rs`

**Purpose**:  
This file provides a mechanism to temporarily disable Tokio's cooperative scheduling constraints for specific futures. It allows wrapping a future to execute without being forced to yield, which can prevent task starvation but risks blocking other tasks if misused.

---

**Key Components**:

1. **`Unconstrained<F>` Struct**:
   - A future wrapper that disables cooperative scheduling for the inner future `F`
   - `#[must_use]` ensures the future is actively polled to take effect
   - Uses `pin_project!` macro for safe pin projection

2. **Conditional `Future` Implementation**:
   - **With Cooperative Scheduling (cfg_coop)**:
     ```rust
     fn poll() {
         crate::task::coop::with_unconstrained(|| inner.poll(cx))
     }
     ```
     Executes the inner future in an "unconstrained" context where budget-based yielding is disabled

   - **Without Cooperative Scheduling (cfg_not_coop)**:
     ```rust
     fn poll() {
         inner.poll(cx)  // No-op wrapper when feature is disabled
     }
     ```

3. **`unconstrained()` Constructor**:
   - Creates an `Unconstrained` wrapper for a given future
   - Public API entry point marked with `#[cfg_attr(docsrs, ...)]` for documentation

---

**Integration with Project**:
- Complements Tokio's cooperative scheduling system (seen in related `Coop` struct)
- Provides an escape hatch for CPU-bound operations or legacy code that can't yield
- Used in scenarios requiring uninterrupted execution at the cost of potential starvation
- Part of the `task::coop` module that manages execution budgeting

---

**Safety Considerations**:
- The documentation explicitly warns about starvation risks
- Should only be used for futures that either:
  - Are guaranteed to complete quickly
  - Contain their own yield points
  - Operate in dedicated runtime threads

---

**Role in Project**:  