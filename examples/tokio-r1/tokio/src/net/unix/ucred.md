# Unix Credentials Handling in Tokio

## Purpose
This file provides cross-platform support for retrieving process credentials (UID, GID, PID) from Unix domain socket connections in the Tokio async runtime. It handles OS-specific implementations while exposing a unified interface.

## Key Components

### 1. UCred Struct
```rust
#[derive(Copy, Clone, Eq, PartialEq, Hash, Debug)]
pub struct UCred {
    pid: Option<unix::pid_t>,
    uid: unix::uid_t,
    gid: unix::gid_t,
}
```
- Stores process credentials with platform-optional PID
- Provides accessor methods (`uid()`, `gid()`, `pid()`)
- Designed to be lightweight (Copy, Clone) for easy passing

### 2. Platform-Specific Implementations
Multiple modules handle different OS variants using conditional compilation:
- **Linux/Android/OpenBSD**: Uses `SO_PEERCRED` socket option
- **macOS/iOS**: Combines `LOCAL_PEEREPID` and `getpeereid`
- **FreeBSD/DragonFly**: Implements `getpeereid` system call
- **Solaris/Illumos**: Uses `getpeerucred` API
- **AIX**: Implements `getpeereid`
- **No-Process Systems**: Fallback with dummy values

### 3. Common Interface
```rust
pub(crate) fn get_peer_cred(sock: &UnixStream) -> io::Result<UCred>
```
- Unified function signature across platforms
- Handles unsafe OS interactions internally
- Converts system errors to Rust's `io::Error`

## Project Integration
- Used by Tokio's Unix domain socket implementation to provide peer credential information
- Enables security-sensitive applications to verify connection origins
- Abstracts away platform differences from higher-level networking code
- Part of Tokio's `net::unix` module architecture

## Implementation Notes
- Heavy use of `cfg` attributes for platform specialization
- Unsafe blocks for low-level system calls
- Type conversions between Rust and C representations
- Error handling through OS error translation
