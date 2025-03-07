### Tokio Runtime Context Error Constants

This file (`error.rs`) serves as a centralized location for error messages related to the Tokio runtime context. It defines three internal constants used to provide consistent and clear error explanations when runtime operations are attempted in invalid states.

#### Key Components
1. **`CONTEXT_MISSING_ERROR`**  
   Explains that a Tokio 1.x runtime context is required but missing. Used when operations (e.g., spawning tasks, timers) are attempted outside a runtime.

2. **`RUNTIME_SHUTTING_DOWN_ERROR`**  
   Indicates the runtime is in shutdown and cannot perform operations like driving timers. Triggered during graceful runtime termination.

3. **`THREAD_LOCAL_DESTROYED_ERROR`**  
   Occurs when the thread-local storage holding the runtime context is destroyed prematurely, often during cleanup of other thread-locals.

#### Features & Compilation
- Uses `#![cfg_attr(...)]` to suppress dead-code warnings when certain features (e.g., `"full"`) are disabled.
- Designed to work across multiple configurations (e.g., WASM targets, unstable features).

#### Relationship to Project
- These errors are referenced throughout Tokio's runtime components (scheduler, task management, I/O drivers) to enforce proper runtime context usage.
- Part of Tokio's internal error handling infrastructure, ensuring consistent messaging for misconfigured runtime access.
- Complements runtime initialization/teardown logic seen in related context snippets (e.g., `runtime::Builder`, thread-local management).

---
