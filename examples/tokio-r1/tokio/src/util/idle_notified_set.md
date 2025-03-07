# `idle_notified_set` Module Explanation

## Purpose
The `idle_notified_set` module defines an `IdleNotifiedSet<T>`, a thread-safe collection for managing asynchronous tasks in two states: 
1. **Notified**: Tasks ready to be polled (their wakers have been triggered).
2. **Idle**: Tasks waiting for external events before progressing.

Its primary role is to efficiently track and transition tasks between these states while minimizing synchronization overhead.

## Key Components

### 1. Core Structures
- **`IdleNotifiedSet<T>`**:  
  Main handle to the collection. Contains:
  - `lists`: Thread-safe shared state (`Arc<Mutex<ListsInner<T>>>`).
  - `length`: Total number of entries across both lists.

- **`ListsInner<T>`**:  
  Inner locked structure holding:
  - `notified`: Linked list of tasks whose wakers have been notified.
  - `idle`: Linked list of inactive tasks.
  - `waker`: Optional waker to notify when tasks move to the `notified` list.

- **`ListEntry<T>`**:  
  Represents an entry in the collection. Contains:
  - `value`: Task data (e.g., `JoinHandle`).
  - `parent`: Reference back to the shared `Lists` structure.
  - `my_list`: Current list membership (`Notified`, `Idle`, or `Neither`).
  - Thread-safe linked list pointers.

### 2. Thread Safety
- Uses `loom` primitives (`Mutex`, `Arc`, `UnsafeCell`) for concurrency control.
- Implements `Send`/`Sync` traits where safe, restricting access to task values via ownership rules.

### 3. Key Operations
- **Insertion** (`insert_idle`):  
  Adds a task to the `idle` list, returning an `EntryInOneOfTheLists` handle.
- **Task Polling** (`pop_notified`):  
  Moves a task from `notified` to `idle` list atomically, allowing safe polling.
- **Iteration** (`for_each`):  
  Applies a function to all tasks in both lists using raw pointers to avoid repeated locking.
- **Draining** (`drain`):  
  Removes all tasks, ensuring cleanup even on panics.

### 4. Waker Integration
- **`Wake` Implementation**:  
  When a task's waker is triggered (`wake_by_ref`), the entry moves from `idle` to `notified` list, notifying the stored waker to schedule polling.

### 5. Safety Mechanisms
- **`EntryInOneOfTheLists`**:  
  Ensures entries remain in valid states by borrowing the set mutably.
- **Linked List Management**:  
  Uses `PhantomPinned` and manual pointer operations to prevent data races and invalid memory access.

## Integration with Tokio
- **Task Scheduling**:  
  Forms the backbone of task scheduling in Tokio's runtime. When tasks are woken (e.g., I/O events), they transition to the `notified` list, allowing the runtime to efficiently poll them.
- **Resource Management**:  
  The `drain` method ensures tasks are cleaned up properly during shutdown, preventing resource leaks.

## Role in the Project