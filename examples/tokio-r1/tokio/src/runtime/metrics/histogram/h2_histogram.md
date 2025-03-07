# Tokio H2 Histogram Implementation

## Purpose
This file implements an H2 Histogram for Tokio's runtime metrics, designed to efficiently track duration distributions with configurable precision and memory usage. It provides a logarithmic-scale histogram optimized for performance while maintaining bounded error margins.

## Key Components

### 1. Core Structures
- **`LogHistogram`**: Main histogram type containing:
  - `num_buckets`: Total bucket count
  - `p`: Precision parameter (error bound = 2^-p)
  - `bucket_offset`: Groups small-value buckets into bucket 0

### 2. Configuration Builder
- **`LogHistogramBuilder`**: Fluent interface for configuration:
  - Sets min/max measurable durations (default: 100ns-60s)
  - Controls precision (default: 25% error)
  - Enforces bucket count limits

### 3. Algorithm Features
- **Bucket Organization**:
  - First bucket covers 0 to `min_value`
  - Last bucket extends to `u64::MAX`
  - Intermediate buckets grow exponentially with precision-controlled grouping
- **Error Guarantee**: Values are placed in buckets with maximum relative error of 2^-p

### 4. Key Methods
- `value_to_bucket()`: Maps duration values to bucket indices
- `bucket_range()`: Returns value range for a given bucket
- `truncate_to_max_value()`: Adjusts bucket count for value constraints

## Integration with Tokio
- Used for runtime metrics collection (e.g., task poll times)
- Configurable via runtime builder APIs
- Balances memory usage (bucket count) with measurement precision
- Replaces legacy histogram implementation with better performance

## Configuration Tradeoffs
- Higher precision (lower `p`) → More buckets → Higher memory usage
- Larger min/max ranges → Fewer buckets → Coarser granularity
- Default configuration uses 119 buckets for 100ns-68s range with 25% error

## Error Handling
- `InvalidHistogramConfiguration`: Thrown when bucket count exceeds limits
- Strict validation of input parameters (non-zero durations, valid precision)

## Testing
- Property-based tests verify:
  - Bucket range continuity
  - Monotonic bucket size growth
  - Error bound compliance
- Spot checks for edge cases and legacy behavior compatibility

# Role in Project