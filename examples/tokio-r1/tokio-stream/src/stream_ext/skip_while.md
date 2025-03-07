# SkipWhile Stream Implementation

## Purpose
This file implements the `SkipWhile` stream combinator for Tokio's asynchronous streams. It provides functionality to skip elements from an underlying stream while a predicate condition holds true, then yields all subsequent elements.

## Key Components

### Struct Definition
- `SkipWhile<St, F>`: Pinned struct containing:
  - `stream`: The underlying stream being wrapped (pinned)
  - `predicate`: Optional closure that determines skipping behavior

### Core Functionality
1. **Polling Logic** (`poll_next`):
   - While predicate exists:
     - Continuously polls underlying stream
     - Skips items while predicate returns `true`
     - Returns first non-matching item and drops predicate
   - After predicate is consumed:
     - Directly delegates to underlying stream

2. **Size Hint Adjustment**:
   - Returns (0, upper_bound) while predicate is active (unknown skipped elements)
   - Returns original stream's size hint after predicate is consumed

3. **Safety & Pin Projection**:
   - Uses `pin_project!` macro for safe pinned projections
   - Maintains proper pinning of underlying stream

### Integration with Stream Ecosystem
- Part of `StreamExt` extension trait methods
- Follows pattern similar to other combinators (`take_while`, `map_while`)
- Maintains Tokio's zero-cost abstraction principles

## Relationship to Project
This implementation is part of Tokio's stream combinator utilities, enabling:
- Functional-style stream processing
- Lazy evaluation of asynchronous data streams
- Composition with other stream operations in the `StreamExt` trait

The file provides a crucial stream transformation primitive that aligns with Rust's iterator combinators but adapted for asynchronous programming patterns.
