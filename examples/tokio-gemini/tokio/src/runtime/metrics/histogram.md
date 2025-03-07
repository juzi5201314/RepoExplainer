这个文件定义了用于 Tokio 运行时度量指标的直方图相关结构和实现。它提供了不同类型的直方图，包括线性直方图和基于 H2 直方图的对数直方图，以及用于构建、批处理和操作这些直方图的工具。

主要组件：

*   **Histogram**:  代表一个直方图，包含桶（buckets）和直方图类型。桶使用 `MetricAtomicU64` 来存储计数，确保线程安全。
*   **HistogramBuilder**:  用于构建直方图的构建器。它允许配置直方图的类型（线性或对数）、桶的数量和桶的宽度。
*   **LegacyBuilder**:  用于配置旧版直方图的构建器，包括分辨率、比例和桶的数量。
*   **HistogramBatch**:  用于批处理直方图数据的结构。它允许在多个值上进行度量，然后将结果提交到 `Histogram`。
*   **HistogramType**:  一个枚举，表示直方图的类型。它支持线性直方图、旧版对数直方图和基于 H2 直方图的对数直方图。
*   **LinearHistogram**:  表示一个线性直方图，具有固定宽度的桶。
*   **LegacyLogHistogram**:  表示一个旧版对数直方图，其中每个桶的大小翻倍。
*   **HistogramScale**:  一个枚举，表示直方图的比例，可以是线性的或对数的。
*   **HistogramConfiguration**:  用于配置轮询计数直方图的结构。

关键功能：

*   **构建直方图**:  `HistogramBuilder` 用于创建不同类型的直方图。
*   **度量值**:  `HistogramBatch` 允许将值添加到直方图中，并计算每个桶的计数。
*   **提交数据**:  `HistogramBatch` 可以将批处理的数据提交到 `Histogram`，更新桶的计数。
*   **桶范围**:  `HistogramType` 提供了 `bucket_range` 方法，用于确定给定桶的范围。
*   **值到桶的映射**:  `HistogramType` 提供了 `value_to_bucket` 方法，用于将值映射到相应的桶。

该文件是 Tokio 运行时度量指标系统的一部分，用于收集和报告关于运行时行为的统计数据，例如延迟和吞吐量。
