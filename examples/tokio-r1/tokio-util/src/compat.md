# Compatibility Layer for `tokio::io` and `futures-io` Traits

## Purpose
This file provides bidirectional compatibility between Tokio's `AsyncRead`/`AsyncWrite` traits and the equivalent `futures-io` traits. It enables interoperability between libraries and components using different async I/O ecosystems.

## Key Components

### 1. `Compat` Wrapper Struct
- **Structure**: Wraps an inner I/O type and tracks seek positions.
- **Functionality**:
  - Implements conversion between `tokio::io` and `futures-io` traits via trait implementations.
  - Maintains seek state for proper async seeking behavior.
  - Provides accessors (`get_ref`, `into_inner`) for the wrapped type.

### 2. Extension Traits
Four extension traits enable seamless conversion:
- `FuturesAsyncReadCompatExt`: Converts `futures_io::AsyncRead` → `tokio::io::AsyncRead`
- `FuturesAsyncWriteCompatExt`: Converts `futures_io::AsyncWrite` → `tokio::io::AsyncWrite`
- `TokioAsyncReadCompatExt`: Converts `tokio::io::AsyncRead` → `futures_io::AsyncRead`
- `TokioAsyncWriteCompatExt`: Converts `tokio::io::AsyncWrite` → `futures_io::AsyncWrite`

Each provides a `compat()` or `compat_write()` method to create the adapter.

### 3. Trait Implementations
- **AsyncRead/AsyncWrite**: Bidirectional conversions handle buffer initialization differences between the ecosystems.
- **AsyncBufRead**: Forwards fill/consume operations.
- **AsyncSeek**: Manages seek state transitions between Tokio's two-phase seeking and futures-io's single-phase model.

### 4. Platform Integrations
- Implements OS-level handle access (`AsRawFd`/`AsRawHandle`) for Unix/Windows compatibility.

## Project Role
This module serves as a critical interoperability layer in Tokio's ecosystem, enabling:
1. Integration of futures-based I/O components with Tokio runtimes
2. Shared usage of I/O types across different async ecosystems
3. Backward compatibility during ecosystem transitions
