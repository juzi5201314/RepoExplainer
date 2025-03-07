这个文件定义了 Tokio 运行时（runtime）的度量指标（metrics）模块，用于收集和展示关于运行时性能的信息。

**主要组成部分：**

1.  **模块声明和导入：**
    *   `mod runtime;` 声明了 `runtime` 子模块，可能包含运行时级别的度量指标。
    *   `pub use runtime::RuntimeMetrics;` 将 `RuntimeMetrics` 结构体导出，供其他模块使用。
    *   `cfg_unstable_metrics! { ... }`：这是一个条件编译块，只有在启用了 `unstable_metrics` 特性时才会被编译。
        *   `mod batch;`、`mod histogram;`、`mod scheduler;`、`mod worker;`、`mod io;` 声明了多个子模块，分别负责批处理、直方图、调度器、工作线程和 I/O 驱动程序的度量指标。
        *   `pub(crate) use ...;` 将这些子模块中的结构体和枚举导出到 crate 内部，供其他模块使用。
        *   `pub use ...;` 将 `HistogramScale`, `HistogramConfiguration`, `LogHistogram`, `LogHistogramBuilder`, `InvalidHistogramConfiguration` 导出到公共 API。
    *   `cfg_not_unstable_metrics! { ... }`：这是另一个条件编译块，在未启用 `unstable_metrics` 特性时编译。
        *   `mod mock;` 声明了一个 `mock` 子模块，可能用于模拟度量指标，方便测试。
        *   `pub(crate) use ...;` 导出 `SchedulerMetrics`, `WorkerMetrics`, `MetricsBatch`, `HistogramBuilder`，供 crate 内部使用。

2.  **条件编译：**
    *   `cfg_unstable_metrics!` 和 `cfg_not_unstable_metrics!` 宏用于根据是否启用了 `unstable_metrics` 特性来选择性地编译代码。这允许在稳定版本中提供有限的度量指标，而在开发版本中提供更详细的指标。

**功能和作用：**

*   **收集运行时信息：** 该模块定义了各种结构体和子模块，用于收集关于 Tokio 运行时各个方面的度量指标，例如任务调度、工作线程负载、I/O 操作等。
*   **提供 API：** 通过 `pub use` 语句，该模块向其他模块提供了访问度量指标的 API，例如 `RuntimeMetrics`、`SchedulerMetrics`、`WorkerMetrics` 等。
*   **支持不稳定特性：** 通过条件编译，该模块可以支持不稳定特性，允许在开发版本中提供更详细的度量指标，而不会影响稳定版本的兼容性。
*   **批处理和直方图：** 模块中包含 `MetricsBatch` 和 `Histogram` 等结构体，用于批处理度量指标和统计数据的分布情况。

**与其他文件的关系：**

*   与 `crate::runtime` 模块紧密相关，因为该模块定义了运行时相关的度量指标。
*   与 `crate::runtime::Builder` 模块相关，因为 `Builder` 允许配置度量指标。
*   与 `crate::runtime::metrics::batch` 模块相关，因为它使用了 `duration_as_u64` 函数。
