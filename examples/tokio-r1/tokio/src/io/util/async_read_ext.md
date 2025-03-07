# Tokio AsyncReadExt Utility Module

## Purpose
This file provides extension methods for the `AsyncRead` trait in Tokio, adding utility functions to read various data types and handle common I/O patterns in asynchronous contexts. It serves as an ergonomic layer that simplifies common operations like reading numeric types, chaining readers, and reading until EOF.

## Key Components

### 1. Core Traits
- **`AsyncReadExt` trait**: Extends `AsyncRead` with 30+ utility methods including:
  - Basic reads (`read`, `read_exact`)
  - Numeric reads (u8-i128, f32/f64 in BE/LE formats)
  - String/buffer operations (`read_to_end`, `read_to_string`)
  - Stream manipulation (`chain`, `take`)

### 2. Macro Generation
- **`read_impl!` macro**: Generates boilerplate for numeric read methods (48 methods total) to handle:
  - Both signed/unsigned integers
  - Big-endian/little-endian formats
  - Floating point numbers
  - Cancel safety documentation

### 3. Important Methods
- **Chaining**: `chain()` combines multiple readers sequentially
- **Buffered Reading**: `read_buf()` for efficient buffer management
- **Exact Reads**: `read_exact()` for fixed-size reads
- **Full Consumption**: `read_to_end()`/`read_to_string()` for complete data consumption
- **Limiting**: `take()` creates a length-limited reader

### 4. Safety & Cancellation
- Documents cancel safety for each operation
- Provides atomicity guarantees for read operations
- Handles error propagation consistently

## Integration with Project
- Part of Tokio's I/O utilities (`io::util` module)
- Complements `AsyncWriteExt` for complete async I/O support
- Used by higher-level components like `tokio::fs::File` and network types
- Integrates with bytes crate's `BufMut` for efficient buffer management

## Example Usage
```rust
use tokio::io::AsyncReadExt;
use tokio::fs::File;

async fn read_file() -> Result<(), std::io::Error> {
    let mut f = File::open("data.bin").await?;
    let version = f.read_u16_le().await?;
    let payload = f.read_to_end().await?;
    Ok(())
}
```

## Key Design Aspects
- Zero-cost abstractions through extension traits
- Type-safe numeric conversions
- Proper handling of async cancellation
- Compatibility with Rust's standard I/O conventions
- Efficient buffer management through `bytes::BufMut`
