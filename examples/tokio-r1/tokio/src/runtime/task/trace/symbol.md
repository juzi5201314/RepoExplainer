### Purpose
This file defines a `Symbol` struct that wraps `backtrace::BacktraceSymbol` to enable hashing, equality checks, and hierarchical tracing in Tokio's task tracing system. It addresses limitations of the underlying backtrace crate by adding unique identification for symbols in call traces.

### Key Components

1. **Symbol Struct**:
   - Contains a `BacktraceSymbol` and `parent_hash` field.
   - `parent_hash` ensures unique identification of symbols in recursive calls or different stack depths.

2. **Trait Implementations**:
   - **Hash**: Combines symbol name bytes, memory address, source location, and parent_hash to create a unique fingerprint.
   - **PartialEq/Eq**: Compares all symbol metadata + parent_hash for equality.
   - **Display**: Formats symbols with simplified names (stripping Rust namespaces) and source locations.

3. **Hierarchical Tracing**:
   - The `parent_hash` creates a chain of responsibility in call traces, enabling differentiation between identical symbols at different call depths.

### Integration with Project
- Works with task tracing infrastructure to track async task execution paths.
- Used in building `SymbolTrace` structures that map to Tokio's task scheduler activities.
- Enables visualization/debugging of task dependencies and execution flows.

### Key Design Choices
- Addresses `backtrace` crate's lack of Hash/Eq implementations
- Uses pointer addresses for symbol identity to handle JIT/optimized code
- Balances human readability (Display impl) with precise machine identification (hashing)
