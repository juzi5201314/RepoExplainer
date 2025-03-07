# Tokio Process Driver Explanation

## Purpose
This file implements a Unix-specific process driver responsible for managing orphaned child processes in Tokio's async runtime. Its primary role is to clean up zombie processes by reaping them after parking operations.

## Key Components

### `Driver` Struct
- **Fields**:
  - `park: SignalDriver`: Handles signal processing and thread parking
  - `signal_handle: SignalHandle`: Provides access to signal handling capabilities
- **Responsibility**: Integrates process management with Tokio's runtime scheduling

### Core Methods
1. `new(park: SignalDriver) -> Self`
   - Constructs a new driver instance by wrapping a signal driver
   - Initializes the signal handle from the provided park

2. `park()` & `park_timeout()`
   - Delegate parking operations to the underlying `SignalDriver`
   - Call `GlobalOrphanQueue::reap_orphans()` after parking to clean up zombie processes
   - `park_timeout` adds duration-based parking capability

3. `shutdown()`
   - Propagates shutdown signals to the underlying park driver

## Integration with Runtime
- Works with Tokio's driver system through `driver::Handle`
- Coordinates with signal handling infrastructure (`SignalDriver`)
- Uses global orphan queue management from `process::unix` module
- Triggered during runtime parking phases to ensure timely process cleanup

## Unix-Specific Behavior
- Conditional compilation using `#[cfg_attr(not(feature = "rt"), allow(dead_code))]`
- Implements proper process lifecycle management required for Unix-like systems
