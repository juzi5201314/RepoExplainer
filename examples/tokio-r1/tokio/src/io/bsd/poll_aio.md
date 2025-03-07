# Tokio POSIX AIO Integration (`poll_aio.rs`)

## Purpose
This module provides integration between POSIX Asynchronous I/O (AIO) and Tokio's async runtime, specifically targeting FreeBSD systems that implement AIO with kqueue notifications. It enables asynchronous handling of AIO operations within Tokio's event-driven architecture.

## Key Components

### 1. `AioSource` Trait
- **Interface Requirement**: Defines methods (`register`, `deregister`) for integrating custom AIO event sources with Tokio's reactor.
- **Usage**: Implemented by types needing to participate in Tokio's async I/O lifecycle.

### 2. `MioSource` Adapter
- **Wrapper**: Bridges `AioSource` implementations to Mio's `Source` trait.
- **Registration Handling**: Translates kqueue registration calls to AIO-specific operations.

### 3. `Aio` Struct
- **Core Type**: Combines a wrapped AIO source (`MioSource`) with Tokio's `Registration` for reactor integration.
- **Key Methods**:
  - `new_for_aio`/`new_for_lio`: Create AIO contexts for different operation types.
  - `poll_ready`: Async polling mechanism for operation completion.
  - `clear_ready`: Manually reset readiness state for edge-triggered scenarios.

### 4. `AioEvent` Type
- **Readiness Token**: Opaque handle representing completed AIO operations, used with `clear_ready`.

## Integration Points
- **Reactor Interaction**: Uses Tokio's `Registration` system to track I/O readiness.
- **Platform Specificity**: Explicitly designed for FreeBSD's kqueue-based AIO implementation.
- **Edge-Triggered Semantics**: Requires careful readiness clearing to avoid starvation.

## Relationship to Project
- **Async Foundation**: Extends Tokio's I/O capabilities to support POSIX AIO operations.
- **BSD Specialization**: Provides platform-specific implementation complementary to Tokio's cross-platform I/O system.
- **Runtime Integration**: Leverages Tokio's scheduler and reactor for efficient async operation management.

---
