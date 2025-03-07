# Code File Explanation: `tokio/src/runtime/metrics/mock.rs`

## Purpose
This file provides **mock implementations** of metrics-related types used in Tokio's runtime. These mocks are designed to replace real metrics-collection logic during testing or when metrics are disabled, ensuring zero runtime overhead while maintaining API compatibility.

## Key Components

### 1. Mock Structs
- **`SchedulerMetrics`**: Tracks scheduler-level metrics (e.g., remote task scheduling). Methods like `inc_remote_schedule_count` are no-ops.
- **`WorkerMetrics`**: Represents per-worker thread metrics. Includes placeholder methods like `set_queue_depth` and `set_thread_id`.
- **`MetricsBatch`**: Aggregates metrics data for submission. Contains stubs for operations like `submit`, `about_to_park`, and task polling tracking.
- **`HistogramBuilder`**: A dummy histogram builder (marked `#[derive(Clone, Default)]`), unused in the mock.

### 2. Conditional Compilation
- The `cfg_rt_multi_thread!` macro adds multi-thread-specific methods to `MetricsBatch` (e.g., `incr_steal_count`), ensuring compatibility with Tokio's multi-threaded runtime mode.

### 3. Testing Utilities
- Methods like `WorkerMetrics::from_config` accept runtime configuration parameters but ignore them, preventing dead-code warnings while mimicking real API usage.
- All methods are empty, avoiding side effects during tests.

## Integration with the Project
- **Testing**: Enables testing of Tokio's runtime components (e.g., schedulers, workers) without metrics overhead or dependencies on real metric collection.
- **Feature Flags**: Works with Tokio's `cfg_unstable_metrics` and runtime configuration flags (e.g., `enable_metrics_poll_time_histogram`), allowing metrics to be conditionally compiled out.
- **API Consistency**: Mirrors the structure of real metrics types in `src/runtime/metrics`, ensuring seamless substitution.

## Role in the Project