# Tokio `read_to_string` Utility Explanation

## Purpose
This file implements an asynchronous `read_to_string` operation for Tokio's I/O utilities. It provides a `Future` that reads all bytes from an `AsyncRead` source into a `String`, handling UTF-8 validation and buffer management efficiently.

## Key Components

### 1. `ReadToString` Future
- **Structure**: Contains references to:
  - The async reader (`reader: &mut R`)
  - Output string (`output: &mut String`)
  - Byte buffer (`buf: VecWithInitialized<Vec<u8>>`)
  - Progress tracking (`read: usize`)
- **Pinning**: Uses `pin_project!` macro for safe pinning with `PhantomPinned`

### 2. Core Functions
- `read_to_string()`: Initializes the operation by:
  1. Taking ownership of the existing string's buffer
  2. Creating a `ReadToString` future with empty buffers
- `read_to_string_internal()`: Core polling logic that:
  1. Uses `read_to_end_internal` to fill byte buffer
  2. Converts bytes to UTF-8 string with validation
  3. Uses `finish_string_read` for error handling and finalization

### 3. Buffer Management
- Utilizes `VecWithInitialized` for efficient buffer handling
- Avoids unnecessary zero-initialization of buffers
- Maintains separation between raw bytes and final string output

### 4. UTF-8 Handling
- Performs validation after reading completes
- Uses `String::from_utf8` for conversion
- Preserves existing string contents if validation fails

## Integration with Tokio
- Part of Tokio's async I/O extension traits (`AsyncReadExt`)
- Complements similar utilities like `read_to_end` and `read_line`
- Uses shared internal components:
  - `read_to_end_internal` for byte reading
  - `finish_string_read` for error handling
- Follows Tokio's pinning patterns for async primitives

## Key Design Choices
1. **Deferred Validation**: Postpones UTF-8 checking until after I/O completes
2. **Buffer Reuse**: Reuses existing string allocation through `mem::take`
3. **Zero-Copy Handling**: Avoids intermediate copies through careful buffer management
