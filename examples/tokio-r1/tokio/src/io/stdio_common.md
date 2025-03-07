# Code File Explanation: `stdio_common.rs`

## Purpose
This file provides a Windows-specific adapter for asynchronous writes to stdout/stderr, ensuring valid UTF-8 output to prevent data corruption. On non-Windows platforms, it acts as a pass-through.

## Key Components

### 1. `SplitByUtf8BoundaryIfWindows` Struct
- **Role**: Wraps an `AsyncWrite` implementation to enforce UTF-8 validity on Windows.
- **Key Logic**:
  - Trims large buffers to `DEFAULT_MAX_BUF_SIZE` (default: 8KB).
  - Detects UTF-8 validity in the first 32 bytes (`MAX_BYTES_PER_CHAR * MAGIC_CONST`).
  - Trims incomplete UTF-8 characters at the end of the buffer to ensure well-formed output.

### 2. Constants
- `MAX_BYTES_PER_CHAR`: Maximum UTF-8 bytes per character (4, per Unicode).
- `MAGIC_CONST`: Determines how much data to check for UTF-8 validity (8x4=32 bytes).

### 3. `poll_write` Method
- **Workflow**:
  1. Skip processing on non-Windows or small buffers.
  2. Trim buffer to `DEFAULT_MAX_BUF_SIZE`.
  3. Check if the buffer starts with valid/incomplete UTF-8.
  4. If UTF-8 is detected, remove trailing bytes of an incomplete character.
  5. Forward the sanitized buffer to the underlying writer.

### 4. Tests
- **`test_splitter`**: Validates correct handling of large UTF-8 buffers.
- **`test_pseudo_text`**: Ensures binary data starting with valid UTF-8 is split correctly without excessive writes.

## Integration with the Project
- Used in Tokio's `Stdout`/`Stderr` implementations (wrapping `Blocking<std::io::Stdout>`).
- Ensures Windows console compatibility by preventing invalid UTF-8 writes.
- Transparently delegates to inner writers on other platforms.

---
