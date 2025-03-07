# Tokio Standard Input (Stdin) Implementation

## Purpose
This file provides an asynchronous interface to the standard input stream (`stdin`) in Tokio. It wraps blocking I/O operations to integrate with async runtime, enabling non-blocking reads while handling platform-specific details for Unix and Windows.

## Key Components

### `Stdin` Struct
- **Wrapper**: Contains a `Blocking<std::io::Stdin>` to manage blocking I/O on a background thread.
- **AsyncRead Implementation**: Delegates to `Blocking`'s async logic, allowing integration with Tokio's async runtime.
- **Caveats**: Designed for non-interactive use (e.g., piped input) due to uncancelable blocking reads that may delay runtime shutdown.

### Constructor (`stdin()`)
- Initializes the async handle using `Blocking::new()`, which safely bridges blocking `std::io::Stdin` to async operations.

### Platform-Specific Traits
- **Unix**: Implements `AsRawFd`/`AsFd` for file descriptor access.
- **Windows**: Implements `AsRawHandle`/`AsHandle` for handle-based I/O.

### Async Integration
- `poll_read` method forwards to the inner `Blocking` type, enabling async reads via Tokio's task scheduling.

## Project Context
- Part of Tokio's I/O module, complementing async stdout/stderr implementations.
- Uses the `Blocking` utility (from `io::blocking`) to offload synchronous I/O to dedicated threads.
- Works alongside other async I/O primitives (e.g., files, pipes) to provide a unified async interface.

## Role in the Project
Provides asynchronous standard input handling for Tokio, enabling stdin interaction in async applications while abstracting OS-specific details and threading complexities.
