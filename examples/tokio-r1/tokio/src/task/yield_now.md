# Tokio `yield_now` Implementation

## Purpose
The `yield_now.rs` file implements the `yield_now()` async function, which allows a Tokio task to voluntarily yield control back to the runtime scheduler. This enables cooperative multitasking by letting other pending tasks execute before the yielding task resumes.

## Key Components

### `yield_now()` Function
- **Entry Point**: A public async function that creates and awaits a `YieldNow` future.
- **Behavior**: When awaited, it temporarily pauses the current task and re-queues it at the end of the scheduler's pending queue.

### `YieldNow` Future
- **State Tracking**: Contains a `yielded: bool` flag to track whether the task has already yielded.
- **Future Implementation**:
  - **Initial Poll**: Marks the task as yielded, defers its rescheduling via `context::defer(cx.waker())`, and returns `Poll::Pending`.
  - **Subsequent Polls**: Returns `Poll::Ready(())` once the task has been rescheduled and re-executed.

### Critical Operations
1. `context::defer(cx.waker())`: 
   - Re-registers the task's waker at the **end** of the scheduler's queue.
   - Ensures other tasks get a chance to run before this task resumes.
2. `crate::trace::trace_leaf(cx)`: 
   - Integrates with Tokio's tracing infrastructure for debugging/task introspection.

## Non-Guarantees (Documentation Notes)
- The runtime may poll the yielding task again immediately if no higher-priority work exists.
- Scheduling order after yielding is not strictly defined and may vary between runtime versions or configurations.

## Relationship to the Project
- **Cooperative Scheduling**: Enables tasks to avoid monopolizing runtime threads, improving fairness.
- **Integration**: Used in Tokio's task utilities (e.g., `spawn`, `select!`) and user code to manage task execution flow.
- **Runtime Context**: Relies on Tokio's internal scheduler context (`context::defer`) for task re-queuing.

---

This file provides the core mechanism for cooperative task yielding in Tokio, enabling efficient concurrency management within the runtime scheduler.  