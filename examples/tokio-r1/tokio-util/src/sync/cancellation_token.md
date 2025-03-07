# `cancellation_token.rs` Explanation

## Purpose
This file implements an asynchronous cancellation mechanism using `CancellationToken`, allowing tasks to cooperatively respond to cancellation requests. It provides structured concurrency patterns for gracefully stopping async operations in Tokio-based applications.

## Key Components

### 1. `CancellationToken` Struct
- **Core Functionality**: Acts as a shared cancellation signal source.
- **Main Methods**:
  - `cancel()`: Triggers cancellation for all linked tokens.
  - `is_cancelled()`: Checks cancellation status.
  - `cancelled()`: Returns a future that resolves when cancellation occurs.
  - `child_token()`: Creates a dependent token that inherits parent cancellation.

### 2. Future Implementations
- `WaitForCancellationFuture`: Borrowed version of cancellation future.
- `WaitForCancellationFutureOwned`: Owned version using `MaybeDangling` for safe self-references.
- `run_until_cancelled()`: Runs a future until either completion or cancellation.

### 3. Internal Mechanisms
- **Tree Structure**: Uses `tree_node::TreeNode` for hierarchical cancellation propagation.
- **Concurrency Safety**: Leverages `loom` for concurrency primitives and `Arc` for shared state.
- **Memory Management**: Implements reference counting with custom `Clone`/`Drop` logic.

## Important Features
- **Cancel Safety**: All operations are designed to be cancellation-safe.
- **Hierarchical Cancellation**: Child tokens inherit parent cancellation without bidirectional coupling.
- **Drop Guarantees**: `DropGuard` ensures cancellation-on-drop behavior.
- **Zero-Cost Wakes**: Efficient notification system using Tokio's `Notified` primitive.

## Integration with Project
- Part of Tokio's synchronization utilities (`tokio-util/src/sync`).
- Used by task management systems like `JoinSet` for cooperative task cancellation.
- Integrates with Tokio's async runtime through notification system.
- Provides foundation for structured concurrency patterns in async Rust.

## Safety Considerations
- Uses `MaybeDangling` to handle self-referential futures safely.
- Implements careful field ordering for proper drop sequence.
- Contains unsafe code with rigorous invariants for static lifetime management.

---
