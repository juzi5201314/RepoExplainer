# Signal Windows Wrappers in Tokio-Stream

## Purpose
This file provides stream adapters for Windows-specific signal handling (`Ctrl+C` and `Ctrl+Break`) in the Tokio async runtime. It wraps low-level signal types from `tokio::signal::windows` to implement the `Stream` trait, enabling integration with Tokio's streaming ecosystem.

## Key Components

### 1. `CtrlCStream`
- **Structure**: Wraps a `CtrlC` signal handler
- **Functionality**:
  - Implements `Stream` to yield `()` values on each received signal
  - Provides conversion methods (`into_inner`, `AsRef`, `AsMut`) for interoperability
- **Usage**: Allows handling CTRL-C events through stream processing:
  ```rust
  let mut stream = CtrlCStream::new(ctrl_c()?);
  while stream.next().await.is_some() {
      // Handle CTRL-C
  }
  ```

### 2. `CtrlBreakStream`
- **Structure**: Wraps a `CtrlBreak` signal handler
- **Mirrors** the same pattern as `CtrlCStream` but for CTRL-BREAK signals
- **Implementation**: Identical stream interface with type-specific conversions

### Core Implementation Details
- **Stream Polling**: Both types delegate to their inner signal's `poll_recv` method
- **Platform Specific**: Enabled only on Windows with `#[cfg_attr(docsrs, doc(cfg(all(windows, feature = "signal"))))]`
- **Zero-Value Streams**: Emit `Some(())` on signal reception rather than carrying data

## Project Integration
- Bridges Tokio's signal handling with the stream abstraction pattern used throughout the ecosystem
- Complements similar Unix signal wrappers in other files
- Enables consistent event processing across different signal types using Tokio's streaming API
