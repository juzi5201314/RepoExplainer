# Tokio Task Tracing Module

## Purpose
This module provides infrastructure for capturing async task execution traces in Tokio's runtime. It enables generating task dumps showing current execution states and backtraces, useful for debugging hanging tasks or analyzing runtime behavior.

## Key Components

### 1. Core Structures
- **`Context`**: Thread-local storage for active tracing state
  - `active_frame`: Intrusive linked list of stack frames
  - `collector`: Accumulates captured backtraces
- **`Frame`**: Represents a stack frame in an intrusive doubly-linked list
- **`Trace`**: Collection of captured backtraces that can be formatted as a tree
- **`Root<T>`**: Future wrapper that establishes tracing boundaries

### 2. Tracing Mechanism
- **`trace_leaf`**: Captures backtraces between `Root` boundary and current execution point
- **Frame Linking**: Maintains parent-child relationships using unsafe pointer operations
- **Conditional Capture**: Only active when tracing context exists

### 3. Runtime Integration
- **Scheduler Support**:
  - `trace_current_thread`: Captures traces for current-thread scheduler
  - `trace_multi_thread`: Captures traces for multi-thread scheduler (feature-gated)
- **Task Processing**:
  - Drains task queues
  - Notifies tasks for tracing
  - Captures traces through `Trace::capture`

### 4. Formatting
- Implements `Display` for `Trace` using tree structure
- Converts raw backtraces to symbolic representations
- Organizes multiple backtraces into hierarchical tree format

## Critical Operations
1. **Tracing Initiation**:
   ```rust
   Trace::capture(|| { /* instrumented code */ })
   ```
2. **Boundary Marking**:
   ```rust
   Root::new(future).await
   ```
3. **Trace Collection**:
   ```rust
   let (result, trace) = Trace::capture(|| my_operation());
   ```

## Integration with Tokio
- Works with both single-threaded and multi-threaded runtimes
- Integrates with task queues and schedulers
- Uses thread-local storage for tracing context
- Maintains low overhead when not actively tracing

## Safety Considerations
- Uses `unsafe` for frame pointer manipulation
- Maintains intrusive linked list invariants
- Handles thread-local destruction cases
- Implements proper memory barriers for cross-thread access
