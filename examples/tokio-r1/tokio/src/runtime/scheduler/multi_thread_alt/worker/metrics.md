### Code File Explanation: `metrics.rs` in Tokio's Multi-Threaded Scheduler

**Purpose**  
This file provides metrics collection utilities for Tokio's alternative multi-threaded scheduler (`multi_thread_alt`). It focuses on tracking queue depths to monitor task distribution across worker threads and the global injection queue.

---

**Key Components**  
1. **Queue Depth Methods**:
   - `injection_queue_depth(&self) -> usize`  
     Returns the number of tasks in the global injection queue (`self.inject.len()`), which holds tasks not yet assigned to specific workers.
   - `worker_local_queue_depth(&self, worker: usize) -> usize`  
     Returns the depth of a specific worker's local stealable task queue (`self.remotes[worker].steal.len()`), used for work-stealing load balancing.

2. **Conditional Metrics**:
   - Wrapped in `cfg_unstable_metrics!` macros, indicating these metrics are part of Tokio's unstable observability features and may require opt-in compilation flags.

3. **Shared State Access**:
   - Both methods operate on the scheduler's `Shared` state, which contains:
     - `inject`: The global task queue.
     - `remotes`: Worker-specific queues accessible to other threads for stealing tasks.

---

**Integration with Project**  
- **Runtime Monitoring**: These metrics enable runtime introspection, helping identify bottlenecks (e.g., overloaded workers or a congested global queue).
- **Work-Stealing Optimization**: The local queue depths inform Tokio's work-stealing algorithm, allowing idle workers to steal tasks from busy ones.
- **Unstable Features**: Part of experimental metrics APIs, reflecting Tokio's phased approach to exposing internal scheduler state.

---

**Role in the Project**  