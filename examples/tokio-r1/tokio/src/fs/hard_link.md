# Tokio `hard_link.rs` Explanation

## Purpose
Provides asynchronous hard link creation functionality as part of Tokio's filesystem operations. Bridges the blocking `std::fs::hard_link` operation into async execution using Tokio's runtime.

## Key Components

### Async Function Signature
```rust
pub async fn hard_link(original: impl AsRef<Path>, link: impl AsRef<Path>) -> io::Result<()>
```
- Accepts path references for both source (`original`) and target (`link`)
- Returns `io::Result<()>` for error handling

### Implementation Strategy
1. **Path Conversion**:
   ```rust
   let original = original.as_ref().to_owned();
   let link = link.as_ref().to_owned();
   ```
   - Converts input paths to owned `PathBuf` for safe move into closure

2. **Async Execution**:
   ```rust
   asyncify(move || std::fs::hard_link(original, link)).await
   ```
   - Uses Tokio's `asyncify` to execute blocking filesystem operation on a dedicated thread
   - Maintains async compatibility without blocking the main runtime

### Platform Behavior
- Unix: Uses `link` system call
- Windows: Uses `CreateHardLink` API
- Maintains compatibility with stdlib's platform-specific behavior

## Integration with Project
- Part of Tokio's filesystem module (`fs`)
- Follows pattern seen in related context for symlink operations
- Complements other async filesystem operations (file I/O, symlinks, etc.)
- Enables async-first filesystem manipulation in Tokio applications

## Error Handling
- Propagates errors from underlying system calls
- Common errors include missing source file or cross-device linking attempts

## Example Usage
```rust
fs::hard_link("a.txt", "b.txt").await?;
```
Creates a hard link from b.txt to a.txt asynchronously.
