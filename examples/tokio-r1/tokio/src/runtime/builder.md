# Tokio Runtime Builder (`builder.rs`)

## Purpose
The `builder.rs` file provides a configurable builder pattern for creating Tokio runtime instances. It allows users to customize various aspects of the runtime, such as thread count, I/O and timer drivers, thread names, stack sizes, and more. The builder supports both single-threaded (current-thread) and multi-threaded runtime configurations.

## Key Components

### `Builder` Struct
- **Runtime Type**: Configured via `kind` (current thread, multi-thread, or experimental multi-thread-alt).
- **Drivers**: Flags for enabling I/O (`enable_io`) and timer (`enable_time`) subsystems.
- **Thread Configuration**: 
  - Worker thread count (`worker_threads`)
  - Max blocking threads (`max_blocking_threads`)
  - Thread naming strategies (`thread_name`)
  - Stack size (`thread_stack_size`)
- **Lifecycle Hooks**: Callbacks for thread start/stop, park/unpark events, and task spawning/termination.
- **Scheduler Tuning**:
  - Global queue polling interval (`global_queue_interval`)
  - Event processing interval (`event_interval`)
  - Local queue capacity (`local_queue_capacity`)
- **Advanced Features**:
  - LIFO slot control (`disable_lifo_slot`)
  - Deterministic RNG seeding (`seed_generator`)
  - Metrics collection (poll time histograms)
  - Unhandled panic handling strategies

### Configuration Methods
- Core setup: `new_current_thread()`, `new_multi_thread()`
- Resource management: `worker_threads()`, `max_blocking_threads()`
- Thread customization: `thread_name()`, `thread_stack_size()`
- Event loop tuning: `global_queue_interval()`, `event_interval()`
- Instrumentation: `on_thread_start()`, `on_thread_park()`, etc.
- Unstable features: `unhandled_panic()`, `disable_lifo_slot()`

### Runtime Construction
- `build()`: Creates a `Runtime` instance based on configuration
- Handles driver initialization (I/O, timer)
- Manages worker thread pools and blocking thread pools
- Configures scheduler implementations (current thread vs multi-thread)

## Project Integration
- **Core Runtime Initialization**: Serves as the entry point for creating all Tokio runtime instances
- **Feature Flag Integration**: Conditionally includes components based on enabled features (e.g., `rt-multi-thread`, `tokio_unstable`)
- **Metrics Collection**: Integrates with Tokio's unstable metrics system when enabled
- **Scheduler Variants**: Supports different scheduler implementations through the `Kind` enum
- **Blocking Pool Management**: Coordinates with separate blocking thread pool implementation

## Example Usage
```rust
let runtime = Builder::new_multi_thread()
    .worker_threads(4)
    .thread_name("my-worker")
    .enable_io()
    .enable_time()
    .build()
    .unwrap();
```

## Role in Project