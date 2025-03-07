# Tokio Runtime Context Management

## Purpose
This file manages thread-local storage of Tokio runtime scheduler contexts, enabling nested runtime entry tracking and ensuring proper context handling for blocking operations. It provides mechanisms to safely set/retrieve the current scheduler handle and enforce guard drop order.

## Key Components

### 1. Core Structures
- **`SetCurrentGuard`**: RAII guard that:
  - Preserves previous scheduler handle
  - Tracks entry depth
  - Enforces thread locality via `PhantomData<SyncNotSend>`
  - Ensures proper context restoration on drop

- **`HandleCell`**: Thread-local storage containing:
  - `RefCell<Option<Handle>>`: Current scheduler handle
  - `Cell<usize>`: Nesting depth counter

### 2. Critical Functions
- **`try_set_current`**: 
  - Sets thread-local scheduler handle
  - Returns guard for automatic cleanup
  - Used when entering runtime contexts

- **`with_current`**:
  - Accesses current handle for closure execution
  - Returns `TryCurrentError` for missing/destroyed contexts
  - Core mechanism for runtime-aware operations

### 3. Safety Mechanisms
- Depth tracking prevents:
  - Overlapping context modifications
  - Incorrect guard drop order (panic if violated)
- Phantom type ensures thread-bound guards
- Atomic context access via `CONTEXT.try_with`

## Integration with Project
- Works with scheduler components (`scheduler::Handle`)
- Supports blocking operations (`block_on`, `block_in_place`)
- Enables runtime entry validation in:
  - Task spawning
  - Async/await execution
  - Interop with synchronous code

## Implementation Details
- **Drop Implementation**: Ensures proper context unwinding even with panics
- **Depth Validation**: Prevents invalid state from nested runtime entries
- **Thread-Local Optimization**: Avoids global locks through per-thread storage

---
