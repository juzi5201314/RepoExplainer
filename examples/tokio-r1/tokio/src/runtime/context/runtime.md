## Tokio Runtime Context Management

### Purpose
This file manages thread-local runtime context entry/exit tracking and resource handling for Tokio's async runtime. It prevents nested runtime usage and maintains per-thread RNG state while ensuring blocking operations are properly tracked.

### Key Components

1. **EnterRuntime Enum**
   - Tracks runtime entry state with two variants:
     - `Entered`: Marks active runtime context with `allow_block_in_place` flag
     - `NotEntered`: Default non-runtime state

2. **EnterRuntimeGuard**
   - RAII guard managing runtime context:
     - `blocking`: Tracks blocking region entry
     - `handle`: Maintains current scheduler handle
     - `old_seed`: Preserves previous RNG seed

3. **enter_runtime Function**
   - Core entry point that:
   - Checks existing context using thread-local storage (CONTEXT)
   - Generates new RNG seed from scheduler's seed generator
   - Creates context guard before executing closure
   - Panics on nested runtime entry attempts

4. **Resource Management**
   - Seed handling preserves/replaces RNG state during context switches
   - Drop implementation ensures proper context cleanup:
     - Resets runtime state
     - Restores original RNG seed

### Integration with Project
- Used by scheduler components like `block_on` and `block_in_place`
- Coordinates with other context modules (blocking regions, task cooperation)
- Forms foundation for thread-local runtime state management
- Enforces runtime safety rules through type system (guards)

### Safety Mechanisms
- `#[track_caller]` for better panic diagnostics
- `must_use` attributes on guards
- Runtime entry checks prevent reentrancy
- Seed management ensures proper randomness isolation

Manages thread entry/exit tracking and resource state for Tokio runtime contexts.  