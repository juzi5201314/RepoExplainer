这个文件定义了 `LogHistogram` 结构体及其相关的构建器和配置，用于在 Tokio 运行时中进行时间度量。`LogHistogram` 是一种基于对数的直方图，类似于 HdrHistogram，但针对性能进行了优化。

**主要组成部分：**

*   **`LogHistogram` 结构体：**
    *   `num_buckets`: 直方图中的桶的数量。
    *   `p`: 直方图的精度，误差上限为 2 的 -p 次方。
    *   `bucket_offset`: 所有索引小于 `bucket_offset` 的桶都归为第 0 个桶。这增加了直方图的最小可测量值。
    *   `Default` trait 的实现：提供默认的 `LogHistogram` 配置。
    *   `from_n_p` 函数：根据 `n` 和 `p` 的值直接创建 `LogHistogram`。
    *   `truncate_to_max_value` 函数：截断直方图，使其最大值不超过指定值。
    *   `builder` 函数：创建一个 `LogHistogramBuilder` 实例。
    *   `max_value` 函数：获取直方图可以存储的最大值。
    *   `value_to_bucket` 函数：将给定的时间值转换为对应的桶索引。
    *   `bucket_range` 函数：获取给定桶的范围。
*   **`LogHistogramBuilder` 结构体：**
    *   用于构建 `LogHistogram` 的配置。
    *   `max_value`: 可选的最大持续时间。
    *   `min_value`: 可选的最小持续时间。
    *   `precision`: 可选的精度。
    *   `max_error` 函数：设置直方图的精度，基于最大误差。
    *   `precision_exact` 函数：直接设置直方图的精度 `p`。
    *   `min_value` 函数：设置直方图可以准确存储的最小持续时间。
    *   `max_value` 函数：设置直方图的最大值。
    *   `max_buckets` 函数：构建直方图，并强制执行最大桶数限制。
    *   `build` 函数：构建 `LogHistogram` 实例。
*   **`InvalidHistogramConfiguration` 枚举：**
    *   表示构建直方图时可能发生的错误。
    *   `TooManyBuckets`: 当直方图需要的桶数超过指定的最大桶数时。
*   **`bucket_index` 函数：**
    *   计算给定值和精度 `p` 组合的桶索引。
*   **测试模块：**
    *   包含各种测试用例，用于验证 `LogHistogram` 的正确性。

**与其他部分的关联：**

*   `LogHistogram` 用于度量 Tokio 运行时中的时间，例如任务的执行时间。
*   `LogHistogramBuilder` 用于配置和创建 `LogHistogram` 实例。
*   `InvalidHistogramConfiguration` 用于处理构建直方图时可能发生的错误。
*   `duration_as_u64` 函数用于将 `Duration` 转换为 `u64`。
*   `MAX_PRECISION` 常量定义了最大的精度。
