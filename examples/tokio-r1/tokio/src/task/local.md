# Tokio Local Task Set (`local.rs`)

## Purpose
The `local.rs` file implements `LocalSet`, a mechanism to execute `!Send` futures on the current thread. It enables spawning and managing non-thread-safe tasks that cannot be moved across threads, such as those using `Rc` or thread-local data.

## Key Components

### 1. **`LocalSet` Struct**
- **Role**: Manages a set of `!Send` tasks bound to the current thread.
- **Fields**:
  - `tick`: Tracks scheduler iterations for task polling fairness.
  - `context`: Thread-local state (tasks, queues) wrapped in `Rc<Context>`.
  - `_not_send`: Ensures `LocalSet` itself is `!Send`.

### 2. **Context Management**
- **`Context`**: Contains shared state (`Arc<Shared>`) and thread-local data.
- **`Shared`**:
  - `local_state`: Thread-specific task queue and ownership metadata.
  - `queue`: Mutex-protected remote task queue for cross-thread scheduling.
  - `waker`: Wakes the `LocalSet` when new tasks are added.
- **Thread-Local Storage**:
  - `CURRENT` thread-local variable stores the active `LocalSet` context.

### 3. **Task Scheduling**
- **`spawn_local`**: Spawns `!Send` futures onto the `LocalSet`, routing them to local/remote queues.
- **`tick()`**: Drives task execution by polling up to `MAX_TASKS_PER_TICK` from local/remote queues.
- **`next_task()`**: Prioritizes tasks from remote/local queues based on a tick interval.

### 4. **Execution Control**
- **`run_until`**: Runs a future to completion while processing spawned local tasks.
- **`block_on`**: Blocks the current thread until a future completes (uses runtime's `block_on`).

### 5. **Thread Safety**
- **`UnsafeCell`/`Mutex`**: Manages concurrent access to task queues.
- **Ownership Checks**: Ensures operations occur only on the thread that created the `LocalSet`.

## Integration with Tokio
- **Runtime Compatibility**: Works with Tokio's single-threaded and multi-threaded runtimes.
- **Task Lifecycle**: Integrates with Tokio's task system (`JoinHandle`, task IDs, tracing).
- **Panic Handling**: Configurable responses to unhandled task panics (shutdown or ignore).

## Example Usage
```rust
let local = LocalSet::new();
local.run_until(async {
    spawn_local(async { /* ... */ }).await.unwrap();
}).await;
```

## Role in Project