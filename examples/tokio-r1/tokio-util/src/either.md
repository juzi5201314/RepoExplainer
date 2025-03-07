# `either.rs` in Tokio-Utils: Type Unification for Async Operations

## Purpose
Provides an `Either<L,R>` enum to unify two different async types (futures, streams, sinks, I/O handles) with identical interfaces. Solves type mismatch issues in conditional async code by creating a common wrapper type.

## Key Components

### 1. Core Enum
```rust
pub enum Either<L, R> {
    Left(L),
    Right(R),
}
```
- Generic wrapper for two potential types
- Derives `Debug` and `Clone`

### 2. Macro Helper
```rust
macro_rules! delegate_call {
    // Boilerplate reduction for trait implementations
}
```
- Safely delegates method calls to wrapped types
- Handles pinning through `Pin::new_unchecked`

### 3. Async Trait Implementations
Implements core async traits by delegation:
- **Future**: `poll()`
- **I/O Traits**: `AsyncRead`, `AsyncWrite`, `AsyncSeek`, `AsyncBufRead`
- **Streams/Sinks**: `futures_core::Stream`, `futures_sink::Sink`

### 4. Testing
Validates functionality with:
- Stream behavior tests
- Async I/O read tests

## Integration with Project

### Relationship to Context
- Complements Tokio's async primitives
- Similar to compatibility wrappers (`Compat`) but more generic
- Enables type-erasure patterns in async code

### Usage Patterns
Solves common async development pain points:
```rust
async fn fetch_data() -> Either<HttpRequest, FileRead> {
    if use_network() {
        Either::Left(http_get())
    } else {
        Either::Right(read_file())
    }
}
```

## Key Features
1. **Trait Transparency**: Wrapped types expose identical interfaces
2. **Zero-Cost Abstraction**: Compiles to same code as direct usage
3. **Ecosystem Compatibility**: Works with Tokio and Futures traits

## Role in Project