# Tokio Runtime Metrics Histogram Implementation

## Purpose
This file provides histogram implementations for collecting and aggregating metrics in Tokio's asynchronous runtime. It supports multiple histogram types (linear, legacy logarithmic, and H2-based logarithmic) to track distributions of values like task poll times or resource usage durations.

## Key Components

### Core Structures
- **`Histogram`**: Main metric container with atomic counters
  - `buckets`: Atomic counters storing frequency counts
  - `histogram_type`: Determines bucket calculation logic
- **`HistogramBuilder`**: Configures histogram properties
  - Supports legacy and modern configuration modes
  - Allows setting resolution, scale type, and bucket count
- **`HistogramBatch`**: Temporary storage for batch updates
  - Reduces atomic operation overhead during metric collection

### Histogram Types
1. **Linear Histogram** (`HistogramType::Linear`)
   - Fixed-width buckets (e.g., 0-100ms, 100-200ms)
2. **Legacy Log Histogram** (`HistogramType::LogLegacy`)
   - Doubling bucket sizes (1, 2, 4, 8...)
3. **H2-based Log Histogram** (`HistogramType::H2`)
   - More sophisticated logarithmic distribution (from `h2_histogram` module)

### Critical Functionality
- **Bucket Calculation** (`value_to_bucket`)
  - Different algorithms per histogram type
  - Uses bit manipulation for logarithmic distributions
- **Range Mapping** (`bucket_range`)
  - Returns value range for each bucket
- **Batch Processing**
  - `HistogramBatch` collects measurements before atomic updates
  - `submit()` transfers batch counts to main histogram

## Integration with Tokio
- Part of runtime metrics system
- Used by components like `RuntimeMetrics` to track:
  - Poll times
  - Task durations
  - Other time-sensitive operations
- Supports both stable and unstable metric APIs
- Integrates with Tokio's atomic metric primitives (`MetricAtomicU64`)

## Configuration Options
```rust
HistogramConfiguration::linear(Duration::from_millis(100), 10)
HistogramConfiguration::log(LogHistogramBuilder::default())
```

## Testing
Comprehensive test suite verifies:
- Bucket boundary calculations
- Measurement distribution across buckets
- Batch submission mechanics
- Legacy and modern configuration paths
- Edge cases (maximum values, bucket overflows)
