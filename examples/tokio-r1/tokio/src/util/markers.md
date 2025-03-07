# markers.rs - Concurrency Marker Types

## Purpose
This file defines marker types used to enforce specific thread safety properties (`Send`/`Sync` traits) in Tokio's concurrency model. These zero-sized types help control synchronization guarantees at compile-time through Rust's type system.

## Key Components

### 1. `SyncNotSend` Marker
```rust
pub(crate) struct SyncNotSend(#[allow(dead_code)] *mut ());
unsafe impl Sync for SyncNotSend {}
```
- **Purpose**: Marks types that are `Sync` (thread-safe shared access) but not `Send` (cannot cross thread boundaries)
- **Mechanism**:
  - Contains a raw pointer (`*mut ()`) which is `!Send`
  - Explicit `Sync` implementation overrides automatic trait derivation
  - Used to wrap types that need thread-shared access without ownership transfer

### 2. `NotSendOrSync` Marker
```rust
cfg_rt! {
    pub(crate) struct NotSendOrSync(#[allow(dead_code)] *mut ());
}
```
- **Purpose**: Marks types that are neither `Send` nor `Sync`
- **Conditional Compilation**:
  - Only available when runtime feature (`cfg_rt`) is enabled
  - Contains a raw pointer preventing both traits
  - Used for thread-local or single-threaded runtime components

## Implementation Details
- **Dead Code Allowances**: `#[allow(dead_code)]` suppresses warnings as these are type system markers rather than runtime values
- **Pointer Usage**: Raw pointers (`*mut ()`) prevent automatic `Send`/`Sync` derivation while avoiding allocation

## Project Integration
These markers are used internally by Tokio to:
1. Enforce thread safety contracts in synchronization primitives
2. Implement custom synchronization logic (e.g., making `!Sync` types safe for sharing)
3. Support conditional compilation of runtime features
4. Work with other concurrency utilities in the `util` module

Related code shows usage patterns in:
- Channel implementations (`Sender`/`Receiver`)
- Async I/O components (`ReadHalf`/`WriteHalf`)
- Task synchronization primitives
