rust
use crate::runtime::metrics::batch::duration_as_u64;
use std::cmp;
use std::error::Error;
use std::fmt::{Display, Formatter};
use std::time::Duration;

const DEFAULT_MIN_VALUE: Duration = Duration::from_nanos(100);
const DEFAULT_MAX_VALUE: Duration = Duration::from_secs(60);

const DEFAULT_PRECISION: u32 = 2;
const MAX_PRECISION: u32 = 10;

/// Log Histogram 实现基于 H2 算法的直方图，用于高效统计时间分布
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub struct LogHistogram {
    pub(crate) num_buckets: usize,
    pub(crate) p: u32,
    pub(crate) bucket_offset: usize,
}

impl Default for LogHistogram {
    fn default() -> Self {
        LogHistogramBuilder::default().build()
    }
}

impl LogHistogram {
    // 参数化构造方法，确保参数有效性
    fn from_n_p(n: u32, p: u32, bucket_offset: usize) -> Self {
        assert!(n >= p);
        let num_buckets = ((n - p + 1) * 1 << p) as usize - bucket_offset;
        Self { num_buckets, p, bucket_offset }
    }

    // 截断最大值以适应配置
    fn truncate_to_max_value(&self, max_value: u64) -> LogHistogram {
        let mut hist = self.clone();
        while hist.max_value() >= max_value {
            hist.num_buckets -= 1;
        }
        hist.num_buckets += 1;
        hist
    }

    // 构造配置构建器
    pub fn builder() -> LogHistogramBuilder {
        LogHistogramBuilder::default()
    }

    // 计算值对应的桶索引
    pub(crate) fn value_to_bucket(&self, value: u64) -> usize {
        let index = bucket_index(value, self.p);
        let offset_bucket = if index < self.bucket_offset as u64 { 0 } else { index - self.bucket_offset as u64 };
        offset_bucket.min(self.num_buckets as u64 - 1) as usize
    }

    // 获取桶对应的数值范围
    pub(crate) fn bucket_range(&self, bucket: usize) -> std::ops::Range<u64> {
        // 实现复杂的指数级范围计算逻辑
        // ...
    }
}

/// 配置构建器，提供灵活的参数设置
#[derive(Default, Debug, Copy, Clone)]
pub struct LogHistogramBuilder {
    max_value: Option<Duration>,
    min_value: Option<Duration>,
    precision: Option<u32>,
}

impl LogHistogramBuilder {
    // 设置最大误差边界
    pub fn max_error(mut self, max_error: f64) -> Self {
        assert!(max_error > 0.0 && max_error < 1.0);
        let mut p = 2;
        while 2_f64.powf(-p as f64) > max_error && p <= MAX_PRECISION {
            p += 1;
        }
        self.precision = Some(p);
        self
    }

    // 直接设置精度参数
    pub fn precision_exact(mut self, p: u32) -> Self {
        assert!(p <= MAX_PRECISION);
        self.precision = Some(p);
        self
    }

    // 构建最终的直方图配置
    pub fn build(&self) -> LogHistogram {
        let p = self.precision.unwrap_or(DEFAULT_PRECISION);
        let min_value = duration_as_u64(self.min_value.unwrap_or(DEFAULT_MIN_VALUE));
        let bucket_offset = cmp::max(bucket_index(min_value, p), 1) - 1;
        let n = max_value.ilog2().max(p) + 1;
        LogHistogram::from_n_p(n, p, bucket_offset as usize).truncate_to_max_value(requested_max_value)
    }
}

// 错误类型，用于配置验证失败时的返回
#[derive(Debug)]
pub enum InvalidHistogramConfiguration {
    TooManyBuckets { required_bucket_count: usize },
}

// 计算桶索引的核心算法
fn bucket_index(value: u64, p: u32) -> u64 {
    if value == 0 { return 0; }
    let h = 63 - value.leading_zeros();
    if h <= p as u32 { value } else {
        let w = h - p as u32;
        ((w as u64 + 1) * (1 << p)) as u64 + ((value - (1_u64 << h)) >> w)
    }
}

// 测试模块验证核心逻辑的正确性
#[cfg(test)]
mod test {
    // 包含多个单元测试和属性驱动测试
}
```

### 文件作用
该文件实现了 Tokio 运行时中用于性能监控的 H2 直方图算法。通过以下核心组件提供高效的时间分布统计能力：

1. **核心结构体**：
   - `LogHistogram`：直方图主体，包含桶数量、精度参数和偏移量
   - `LogHistogramBuilder`：配置构建器，提供灵活的参数设置接口

2. **关键功能**：
   - **动态范围调整**：通过 `bucket_offset` 跳过不必要的小时间间隔，减少存储开销
   - **误差控制**：通过精度参数 `p` 控制误差边界（2^-p），默认 25% 误差
   - **范围计算**：指数级扩展的桶范围设计，支持从纳秒到最大值（默认 60 秒）的宽泛时间跨度

3. **算法特性**：
   - 桶范围按指数增长，保证存储效率
   - 支持最大值截断和无限大范围（最后一桶覆盖到 u64::MAX）
   - 通过 `bucket_index` 算法实现 O(1) 时间复杂度的值到桶映射

### 在项目中的角色