# Tokio Stream Extension Combinators (`stream_ext.rs`)

## Purpose
This file implements the `StreamExt` trait, providing a comprehensive set of combinator methods for working with asynchronous streams in Tokio. It extends the base `Stream` trait with functionality similar to Rust's iterator combinators, enabling stream transformation, filtering, merging, and error handling in async contexts.

## Key Components

### Core Structure
- **Combinator Modules**: Contains 20+ submodules (`map`, `filter`, `merge`, etc.) implementing specific stream operations
- **Conditional Time Features**: Time-based operations (`timeout`, `throttle`) gated behind `cfg_time!` macro
- **Trait Implementation**: `StreamExt` trait with default method implementations for all `Stream` types

### Main Functionality
1. **Core Operations**:
   - Element access (`next`, `try_next`)
   - Transformation (`map`, `then`, `map_while`)
   - Filtering (`filter`, `filter_map`)
   - Flow control (`take`, `skip`, `fuse`)
   - Combination (`chain`, `merge`)

2. **Terminal Operations**:
   - Aggregation (`fold`, `collect`)
   - Boolean checks (`all`, `any`)

3. **Time-sensitive Operations** (feature-gated):
   - Timeouts (`timeout`, `timeout_repeating`)
   - Rate limiting (`throttle`)
   - Batched collection (`chunks_timeout`)

4. **Utility Features**:
   - Peekable streams (`peekable`)
   - Size hint merging (`merge_size_hints`)

## Key Methods
| Method Category       | Notable Methods                          |
|-----------------------|------------------------------------------|
| Element Access        | `next()`, `try_next()`                   |
| Transformation        | `map()`, `then()`, `map_while()`         |
| Filtering             | `filter()`, `filter_map()`               |
| Flow Control          | `take()`, `skip()`, `fuse()`             |
| Combination           | `chain()`, `merge()`                     |
| Time Management       | `timeout()`, `throttle()`, `chunks_timeout()` |
| Terminal Operations   | `fold()`, `collect()`, `all()`, `any()`  |

## Integration with Project
- **Core Stream Handling**: Serves as the primary interface for stream manipulation in Tokio
- **Interoperability**: Designed to complement (but not conflict with) `futures::StreamExt`
- **Feature Extensibility**: Time-related operations conditionally compiled via `cfg_time!`
- **Ecosystem Foundation**: Underpins higher-level stream processing in Tokio's async runtime

## Example Usage Patterns
```rust
// Basic stream processing
stream.filter(|x| x % 2 == 0)
      .map(|x| x * 2)
      .take(5)
      .collect::<Vec<_>>()

// Time-sensitive processing
stream.timeout(Duration::from_secs(1))
      .throttle(Duration::from_millis(100))
```

## Role in Project